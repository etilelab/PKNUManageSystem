# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BestCustomer(models.Model):
    customer = models.OneToOneField('Customers', models.DO_NOTHING, primary_key=True)
    best_date = models.CharField(max_length=255)
    best_rank = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'best_customer'
        unique_together = (('customer', 'best_date'),)


class BestEmployee(models.Model):
    employee = models.OneToOneField('Employees', models.DO_NOTHING, primary_key=True)
    best_date = models.CharField(max_length=255)
    best_rank = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'best_employee'
        unique_together = (('employee', 'best_date'),)


class Board(models.Model):
    write_id = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=2000)
    employee = models.ForeignKey('Employees', models.DO_NOTHING)
    write_date = models.DateTimeField(blank=True, null=True)
    notice = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'board'


class Contacts(models.Model):
    contact_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    customer = models.ForeignKey('Customers', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contacts'


class Countries(models.Model):
    country_id = models.CharField(primary_key=True, max_length=2)
    country_name = models.CharField(max_length=40)
    region = models.ForeignKey('Regions', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries'


class Customers(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employees(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    hire_date = models.DateTimeField()
    manager = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    job_title = models.CharField(max_length=255)
    credit_limit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employees'


class Inventories(models.Model):
    product = models.OneToOneField('Products', models.DO_NOTHING, primary_key=True)
    warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING)
    quantity = models.IntegerField()

    def purchase(self, quantity=1):
       self.quantity = self.quantity - quantity

    class Meta:
        managed = False
        db_table = 'inventories'
        unique_together = (('product', 'warehouse'),)


class Locations(models.Model):
    location_id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(Countries, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'locations'


class Member(models.Model):
    email = models.CharField(primary_key=True, max_length=50)
    passwd = models.CharField(max_length=255)
    employee = models.ForeignKey(Employees, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'member'


class OrderItems(models.Model):
    order = models.OneToOneField('Orders', models.DO_NOTHING, primary_key=True)
    item_id = models.IntegerField()
    product = models.ForeignKey('Products', models.DO_NOTHING)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'order_items'
        unique_together = (('order', 'item_id'),)


class Orders(models.Model):
    order_id = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=20)
    salesman = models.ForeignKey(Employees, models.DO_NOTHING, blank=True, null=True)
    order_date = models.DateTimeField()
    employee_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'orders'


class ProductCategories(models.Model):
    category_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'product_categories'


class Products(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000, blank=True, null=True)
    standard_cost = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    list_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(ProductCategories, models.DO_NOTHING)
    likes = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    discount_price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class Regions(models.Model):
    region_id = models.IntegerField(primary_key=True)
    region_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'regions'


class Warehouses(models.Model):
    warehouse_id = models.IntegerField(primary_key=True)
    warehouse_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'warehouses'
