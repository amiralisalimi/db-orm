from peewee import *

database = PostgresqlDatabase(None)

class BaseModel(Model):
    class Meta:
        database = database

class PointField(Field):
    field_type = 'point'

    def db_value(self, value):
        return fn.ST_GeomFromGeoJSON(value)

    def python_value(self, value):
        return fn.ST_AsGeoJSON(value)

class Citizen(BaseModel):
    ssn = CharField(max_length=10, primary_key=True)
    dob = DateField()
    fname = CharField(max_length=256)
    lname = CharField(max_length=256)
    gender = CharField(max_length=10)
    supervisor = CharField(max_length=10)

class CitizenAccount(BaseModel):

    class Meta:
        primary_key = CompositeKey('ssn', 'acc_no')
        table_name = 'citizen_acc'

    ssn = ForeignKeyField(Citizen, backref='accounts', column_name='ssn')
    acc_no = CharField(max_length=16)
    balance = IntegerField()

class Transportation(BaseModel):
    trid = IntegerField(primary_key=True)
    type = CharField(max_length=10)

class Car(BaseModel):
    cid = IntegerField(primary_key=True)
    color = CharField(max_length=32)
    brand = CharField(max_length=32)

class PublicCar(BaseModel):

    class Meta:
        table_name = 'public_car'

    cid = ForeignKeyField(Car, backref='public_cars', column_name='cid', primary_key=True)
    trid = ForeignKeyField(Transportation, backref='public_cars', column_name='trid')
    driver = ForeignKeyField(Citizen, backref='public_car_drives', column_name='driver')

class Station(BaseModel):
    sid = IntegerField(primary_key=True)
    name = CharField(max_length=256)
    loc = PointField()

class History(BaseModel):
    code = CharField(max_length=32, primary_key=True)

class Parking(BaseModel):
    pid = IntegerField(primary_key=True)
    cost = IntegerField()
    name = CharField(max_length=256)
    capacity = IntegerField()
    start_time = TimeField()
    end_time = TimeField()
    loc = PointField()

class ParkingReceipt(BaseModel):

    class Meta:
        table_name = 'parking_receipt'
    
    history_code = ForeignKeyField(History, backref='parking_receipts', column_name='history_code', primary_key=True)
    car = ForeignKeyField(Car, backref='parking_receipts', column_name='car')
    driver = ForeignKeyField(Citizen, backref='parking_receipts', column_name='driver')
    pid = ForeignKeyField(Parking, backref='parking_receipts', column_name='pid')
    prid = IntegerField(unique=True)
    cost = IntegerField()
    exit_time = DateTimeField()
    enter_time = DateTimeField()

class Home(BaseModel):
    hid = IntegerField(primary_key=True)
    owner = ForeignKeyField(Citizen, backref='homes', column_name='owner')
    address = CharField(max_length=256)
    loc = PointField()

class Path(BaseModel):
    pid = IntegerField(primary_key=True)
    name = CharField(max_length=256)

class Trip(BaseModel):
    trip_code = CharField(max_length=32, primary_key=True)
    driver = ForeignKeyField(Citizen, backref='trips', column_name='driver')
    car = ForeignKeyField(Car, backref='trips', column_name='car')
    path = ForeignKeyField(Path, backref='trips', column_name='path')

class TripReceipt(BaseModel):

    class Meta:
        table_name = 'trip_receipt'
    
    history_code = ForeignKeyField(History, backref='trip_receipts', column_name='history_code', primary_key=True)
    start_station = ForeignKeyField(Station, backref='trip_receipts_start_station', column_name='start_station')
    end_station = ForeignKeyField(Station, backref='trip_receipts_end_station', column_name='end_station')
    ssn = ForeignKeyField(Citizen, backref='trip_receipts', column_name='ssn')
    trip_code = ForeignKeyField(Trip, backref='trip_receipts', column_name='trip_code', unique=True)
    cost = IntegerField()
    start_time = DateTimeField()
    end_time = DateTimeField()

class UrbanService(BaseModel):
    
    class Meta:
        table_name = 'urban_service'
    
    usid = IntegerField(primary_key=True)
    type = CharField(max_length=16)

class UrbanServiceReceipt(BaseModel):

    class Meta:
        table_name = 'urban_service_receipt'
    
    history_code = ForeignKeyField(History, backref='urban_service_receipts', column_name='history_code', primary_key=True)
    owner = ForeignKeyField(Home, backref='urban_service_receipts', column_name='owner')
    usid = ForeignKeyField(UrbanService, backref='urban_service_receipts', column_name='usid')
    code = CharField(max_length=32, unique=True)
    date = DateTimeField()
    usage = IntegerField()
    cost = IntegerField()
