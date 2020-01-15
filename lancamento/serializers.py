from rest_framework import serializers
from .models import TipoLancamento, Lancamento, Receita, LancamentoItem
from rest_framework.utils import model_meta


class TipoLancamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoLancamento
        fields = '__all__'


class LancamentoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LancamentoItem
        fields = ('id', 'descricao', 'valor')


class LancamentoSerializer(serializers.ModelSerializer):
    itenslancamento = LancamentoItemSerializer(many=True)

    class Meta:
        model = Lancamento
        fields = '__all__'

    def create(self, validated_data):
        itenslancamento_data = validated_data.pop('itenslancamento')
        lancamento = Lancamento.objects.create(**validated_data)
        for item_data in itenslancamento_data:
            LancamentoItem.objects.create(
                lancamento=lancamento, **item_data)
        return lancamento
    
    def update(self, instance, validated_data):
        itenslancamento_data = validated_data.pop('itenslancamento')
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        for item_rec in itenslancamento_data:
            try:
                item_lancamento_db = LancamentoItem.objects.get(
                    lancamento=instance, descricao=item_rec["descricao"])
                item_lancamento_db.descricao = item_rec["descricao"]
                item_lancamento_db.valor = item_rec["valor"]
                item_lancamento_db.save()
            except LancamentoItem.DoesNotExist:
                LancamentoItem.objects.create(
                    lancamento=instance, **item_rec)
            except LancamentoItem.MultipleObjectsReturned:
                LancamentoItem.objects.filter(
                    lancamento=instance, descricao=item_rec["descricao"]).delete()
                LancamentoItem.objects.create(
                    lancamento=instance, **item_rec)

        itens_lancamento_db = LancamentoItem.objects.filter(
            lancamento=instance)
        for item_lancamento_rec_db in itens_lancamento_db:
            is_deleted = True
            for item_lancamento_rec in itenslancamento_data:
                if (item_lancamento_rec["descricao"] == item_lancamento_rec_db.descricao):
                    is_deleted = False
                    break
            if is_deleted:
                LancamentoItem.objects.get(
                    id=item_lancamento_rec_db.id).delete()

        instance.save()
        return instance



class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = '__all__'