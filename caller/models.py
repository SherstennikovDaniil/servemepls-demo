from django.db import models
import uuid
import base62


# Create your models here.
class Restaurant(models.Model):
    restaurant = models.CharField('Front название', max_length=100,
                                  help_text='Название, которое отображается на странице.')
    back_identif = models.CharField('Back название', max_length=300, blank=True, null=True,
                                    help_text='Оставить пустым!!!')
    address = models.CharField('Адрес', max_length=300)
    phone = models.CharField('Телефон', max_length=17)
    name = models.CharField('Имя', max_length=100)
    vk = models.URLField('VK', blank=True, null=True)
    inst = models.URLField('Inst', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.back_identif = self.restaurant + ' ' + self.address
        super(Restaurant, self).save(*args, **kwargs)

    def __str__(self):
        return self.back_identif


class Waiter(models.Model):
    rest = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField('Имя', max_length=300)
    telegram_id = models.BigIntegerField('Telegram ID')
    tables = models.CharField('Столы', max_length=200, null=True)

    def save(self, *args, **kwargs):
        super(Waiter, self).save(*args, **kwargs)
        tbls = str(self.tables).split(', ')
        for tbl in tbls:
            if '-' in tbl:
                for num in range(int(tbl.split('-')[0]), int(tbl.split('-')[1]) + 1):
                    if not Table.objects.filter(number=num, rest=self.rest):
                        table = Table()
                        table.number = num
                        table.waiter = self
                        table.rest = self.rest
                        table.save()
                    else:
                        Table.objects.filter(number=num, rest=self.rest).update(waiter=self)
            else:
                if not Table.objects.filter(number=tbl, rest=self.rest).update(waiter=self):
                    table = Table()
                    table.number = tbl
                    table.waiter = self
                    table.rest = self.rest
                    table.save()
                else:
                    Table.objects.filter(number=tbl, rest=self.rest).update(waiter=self)

    def __str__(self):
        return self.name


class Table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    number = models.IntegerField('Номер стола')
    slug = models.CharField('Slug столы', max_length=300, blank=True, null=True, unique=True)
    waiter = models.ForeignKey(Waiter, on_delete=models.CASCADE, null=True)
    rest = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    url = models.URLField('Ссылка', null=True)
    qr = models.URLField('QR', null=True)

    def save(self, *args, **kwargs):
        self.slug = base62.encodebytes(str(uuid.uuid1()).encode())
        self.url = 'https://servemepls.ru/caller/' + self.slug
        self.qr = f'https://api.qrserver.com/v1/create-qr-code/?size=404x404&data={self.url}'
        super(Table, self).save(*args, **kwargs)

    def __str__(self):
        return self.rest.back_identif


class Log(models.Model):
    date = models.DateTimeField('Дата', auto_now=True)
    restaurant = models.CharField('Ресторан', max_length=300, null=True)
    table = models.IntegerField('Номер столика', null=True)

    def __str__(self):
        return self.restaurant
