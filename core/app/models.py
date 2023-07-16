from tortoise import fields, models


class Cargo(models.Model):
    id = fields.IntField(pk=True)
    cargo_type = fields.CharField(max_length=120, unique=True)
    cargo_price = fields.FloatField()

    def __str__(self):
        return f'{self.id} {self.cargo_type} {self.cargo_price}'

    class Meta:
        table = "Cargo"
