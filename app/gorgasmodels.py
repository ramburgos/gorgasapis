from sqlalchemy import Column, Integer, Date, String, DateTime,Time,Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import ChoiceType
from enum import Enum

Base=declarative_base()

class pagojornadaextraordinaria_choices(Enum):
    Pago_como_Compensatorio = 1
    Pago_en_Efectivo = 2


class pagolicencia_choices(Enum):
    Ninguno = 0
    Pago_Regular = 1
    Pago_a_Persona_Autorizada = 2
    Pago_a_Cuenta_Bancaria = 3

class tipolicencia_choices(Enum):
    Sin_Sueldo = 1
    Con_Sueldo = 2
    Especial = 3

class pagovacacion_choices(Enum):
    Pago_Regular = 1
    Pago_Adelantado = 2

class quincenas_choices(Enum):
    Ninguna = 0
    Primera_Quincena = 1
    Segunda_Quincena = 2

class meses_choices(Enum):
    Ninguno = 0 
    enero = 1
    febrero =2 
    marzo = 3
    abril = 4
    mayo = 5
    junio = 6
    julio = 7
    agosto = 8
    septiembre = 9
    octubre = 10
    noviembre = 11
    diciembre = 12

estadosolicitudes_choices={
    (0,"Borrador"),
    (1,"Por autorizar Jefe"),
    (2,"Por aprobar OIRH"),
    (3,"Aprobado"),
    (4,"No Aprobado"),   
}
 
class CivilStatus(Base):
    __tablename__ = 'gorgashumanresource_civilstatus'
    civilstatus_id = Column(Integer,primary_key=True)
    descripcion = Column(String)
    
class BloodType(Base):
    __tablename__= 'gorgashumanresource_bloodtype'
    bloodtype_id = Column(Integer,primary_key=True)
    descripcion = Column(String)    

class ScholarShip(Base):
    __tablename__= 'gorgashumanresource_scholarship'
    scholarship_id = Column(Integer,primary_key=True)
    descripcion = Column(String)  

class Types(Base):
    __tablename__= 'gorgashumanresource_types'
    types_id=Column(Integer,primary_key=True)
    descripcion=Column(String)

class MotivePermission(Base):
    __tablename__= 'gorgashumanresource_motivepermission'
    motivepermission_id = Column(Integer,primary_key=True)
    descripcion = Column(String)  

class MotiveLicense(Base):
    __tablename__= 'gorgashumanresource_motivelicense'
    motivelicense_id= Column(Integer,primary_key= True)
    descripcion = Column(String)
        
class JobsType(Base):
    __tablename__= 'gorgashumanresource_jobstype'
    jobstype_id=Column(Integer,primary_key=True)
    descripcion=Column(String)

class Jobs(Base):
    __tablename__= 'gorgashumanresource_jobs'
    jobs_id=Column(Integer,primary_key=True)
    codigo = Column(String)
    jobstype_id= Column(Integer,ForeignKey('gorgashumanresource_jobstype.jobstype_id'))
    descripcion=Column(String)

class CountryUbications(Base):
    __tablename__= 'gorgashumanresource_countryubications'
    countryubications_id=Column(Integer,primary_key=True)
    descripcion=Column(String)

class Employees(Base):
    __tablename__= 'gorgashumanresource_employees'
    employee_id = Column(Integer,primary_key=True)
    cedula = Column(String)
    nombre1 = Column(String)
    apellido1 = Column(String)
    email = Column(String)
    email_inst = Column(String)
    paisnacimiento = Column(String)
    nacimiento=Column(String)
    direccion=Column(String)
    direccionsecundaria = Column(String)
    telefono=Column(String)
    contacto_nombre=Column(String)
    contacto_telefono=Column(String)
    madre_nombre=Column(String)
    padre_nombre=Column(String)
    hijos=Column(Integer)
    civilstatus_id=Column(Integer,ForeignKey("gorgashumanresource_civilstatus.civilstatus_id"))
    conyuge_nombre=Column(String)
    bloodtype_id=Column(Integer,ForeignKey("gorgashumanresource_bloodtype.bloodtype_id"))
    seguro=Column(String)
    scholarship_id=Column(Integer,ForeignKey("gorgashumanresource_scholarship.scholarship_id"))
    profesion=Column(String)
    idoneidad=Column(String)
    foto=Column(String)
    

class AppUser(Base):
    __tablename__ = 'gorgasapp_appuser'
    id= Column(Integer, primary_key=True)
    password= Column(String)
    estado=Column(Integer)
    employee_id= Column(Integer,ForeignKey("gorgashumanresource_employees.employee_id"))
    
        
class Markings(Base):
    __tablename__ = 'gorgashumanresource_markings'
    id= Column(Integer, primary_key=True)
    user_id = Column(Integer)
    registro =Column(String)
    assignments_id =Column(Integer)
    devices_id = Column(Integer)


class Uadministrativas(Base):
    __tablename__= 'gorgashumanresource_uadministrativas'
    id=Column(Integer, primary_key=True)
    nombre= Column(String)
    parent_id = Column(Integer)

class Contracts(Base):  
    __tablename__ = 'gorgashumanresource_contracts'
    contracts_id=Column(Integer,autoincrement=True,primary_key=True)
    resolucion= Column(String)
    fecharesolucion =Column(String)
    fechafirmacontrato =Column(String)
    motivocontrato= Column(Integer,ForeignKey("gorgashumanresource_employees.employee_id"))
    planilla=Column(Integer)
    employee = Column(Integer,ForeignKey("gorgashumanresource_employees.employee_id"))
    jeferecursohumano = Column(Integer,ForeignKey("gorgashumanresource_employees.employee_id"))
    directorgeneral = Column(Integer,ForeignKey("gorgashumanresource_employees.employee_id"))
    nombreministro= Column(String)
    cedulaministro= Column(String)
    posicion = Column(Integer)
    salario = Column(String)
    sobresueldo = Column(String)
    gastorepresentacion= Column(String)
    siacap = Column(Integer)
    vigenciasalariodesde = Column(String)
    cuenta= Column(String)
    fechadesde = Column(String)
    fechahasta = Column(String)
    #impuestofiscalmensual = Column(bool)
    diaspermiso = Column(Integer)
    diaspermisoproporcional = Column(Integer)
    diasvacaciones = Column(Integer)
    mesdiaresolucionvacacion = Column(String)
    jobs_id= Column(Integer,ForeignKey("gorgashumanresource_jobs.jobs_id"))
    uadministrativa_id = Column(Integer,ForeignKey("gorgashumanresource_uadministrativas.id"))
    countryubications_id = Column(Integer,ForeignKey("gorgashumanresource_countriubications.countryubications_id"))
    types_id = Column(Integer,ForeignKey("gorgashumanresource_types.types_id"))
    #designacionsuperior = Column(bool)
    observacion= Column(String)
    estado=Column(Integer)
    

class Permissions(Base):
    __tablename__ = 'gorgashumanresource_permissions'
    permissions_id=Column(Integer, primary_key=True)
    employee_id = Column(Integer,ForeignKey('gorgashumanresource_employees.employee_id'))
    contracts_id= Column(Integer,ForeignKey('gorgashumanresource_contracts.contracts_id'))
    motivepermission_id = Column(Integer,ForeignKey('gorgashumanresource_motivepermission.motivepermission_id'))
    observacion= Column(String)
    fechadesde=Column(Date)
    horadesde= Column(Time)
    fechahasta=Column(Date)
    horahasta=Column(Time)
    horastomadas=Column(String)
    estado=Column(Integer)
    created_by=Column(String)
    created_at=Column(DateTime)
    updated_by=Column(String)
    updated_at=Column(DateTime)
    approved_by = Column(String)
    approved_at = Column(DateTime)
    validated_by = Column(String)
    validated_at = Column(DateTime)

class Vacations(Base):
    __tablename__= 'gorgashumanresource_vacations'
    vacations_id=Column(Integer,primary_key=True)
    employee_id = Column(Integer,ForeignKey('gorgashumanresource_employees.employee_id'))
    contracts_id= Column(Integer,ForeignKey('gorgashumanresource_contracts.contracts_id'))
    proporcional = Column(Boolean)
    observacion = Column(String)
    tomardesde = Column(Date)
    tomarhasta = Column(Date)
    tomadosdesde = Column(Date)
    tomadoshasta = Column(Date)
    diastomados = Column(Integer)
    diasatomar = Column(Integer)
    fechareintegrosolicitud = Column(Date)
    fechareintegroregistrada = Column(Date)
    pagovacacion = Column(ChoiceType(pagovacacion_choices))
    quincenapagovacacion= Column(ChoiceType(quincenas_choices))
    mespagovacacion= Column(ChoiceType(meses_choices))
    anopagovacacion= Column(Integer)
    estado = Column(Integer)
    created_by=Column(String)
    updated_by=Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    approved_by = Column(String)
    approved_at = Column(DateTime)
    validated_by = Column(String)
    validated_at = Column(DateTime)

class Licenses(Base):
    __tablename__= 'gorgashumanresource_licenses'
    licenses_id = Column(Integer,primary_key=True)
    employee_id = Column(Integer,ForeignKey('gorgashumanresource_employees.employee_id'))
    contracts_id= Column(Integer,ForeignKey('gorgashumanresource_contracts.contracts_id'))
    tipo = Column(ChoiceType(tipolicencia_choices))
    motivelicense_id = Column(Integer,ForeignKey('gorgashumanresource_motivelicense.motivelicense_id'))
    fechadesde = Column(Date)
    fechahasta = Column(Date)
    diasportomar = Column(Integer)
    documentocss = Column(String)
    pagolicencia = Column(ChoiceType(pagolicencia_choices))
    nombrebanco = Column(String)
    cuentabancaria = Column(String)
    estado = Column(Integer)
    created_by = Column(String)
    updated_by = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    approved_by = Column(String)
    approved_at = Column(DateTime)
    validated_by = Column(String)
    validated_at = Column(DateTime)

class LicensesResolutions(Base):
    __tablename__= 'gorgashumanresource_licensesresolutions'
    licensesresolutions_id = Column(Integer,primary_key=True)
    licenseresolution = Column(String)
    licenses_id= Column(Integer,ForeignKey('gorgashumanresource_licenses.licenses_id'))
    fecharesolucionlicencia = Column(String)
    observacionlicencia= Column(String)
    articulosegundo=Column(String)
    created_by = Column(String)
    updated_by = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    validated_by = Column(String)
    validated_at = Column(String)



class VacationsResolutions(Base):
    __tablename__= 'gorgashumanresource_vacationsresolutions'
    vacationsresolutions_id = Column(Integer,primary_key=True)
    vacationresolution = Column(String)
    employee_id = Column(Integer,ForeignKey('gorgashumanresource_compensatories.employee_id'))
    contracts_id = Column(Integer,ForeignKey('gorgashumanresource_compensatories.contracts_id'))
    fecharesolucionvacacion = Column(String)
    created_by = Column(String)
    updated_by = Column(String)
    created_at = Column(String)
    updated_at = Column(String)

class VacationsResolutionsVigencies(Base):
    __tablename__= 'gorgashumanresource_vacationsresolutionsvigencies'
    vacationsvigencies_id = Column(Integer,primary_key=True)
    vacationsresolutions_id = Column(Integer,ForeignKey('gorgashumanresource_vacationsresolutions.vacationsresolutions_id'))
    vigenciadesde = Column(String)
    vigenciahasta = Column(String)
    diasresueltos = Column(Integer)
    ajustediasresueltos = Column(Integer)

class Journeys(Base):
    __tablename__= 'gorgashumanresource_journeys'
    journeys_id=Column(Integer,primary_key=True)
    employee_id = Column(Integer,ForeignKey('gorgashumanresource_employees.employee_id'))
    contracts_id= Column(Integer,ForeignKey('gorgashumanresource_contracts.contracts_id'))
    observacion= Column(String)
    fechadesde=Column(Date)
    fechahasta=Column(Date)
    horaspreviasentrada=Column(Boolean)
    estado=Column(Integer)
    created_by=Column(String)
    updated_by=Column(String)
    created_at=Column(DateTime)
    updated_at=Column(DateTime)
    approved_by=Column(String)
    approved_at=Column(DateTime)
    validated_by=Column(String)
    validated_at=Column(DateTime)
    
class Compensatories(Base):
    __tablename__= 'gorgashumanresource_compensatories'
    compensatories_id=Column(Integer,primary_key=True)
    employee_id = Column(Integer,ForeignKey('gorgashumanresource_employees.employee_id'))
    contracts_id= Column(Integer,ForeignKey('gorgashumanresource_contracts.contracts_id'))
    observacion =Column(String) 
    fechadesde = Column(DateTime)
    horadesde = Column(Time)
    fechahasta = Column(Date)
    horahasta = Column(Time)
    horastotales = Column(Integer)
    estado = Column(Integer)
    created_by = Column(String)
    updated_by = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    approved_by = Column(String)
    approved_at = Column(DateTime)
    validated_by = Column(String)
    validated_at = Column(DateTime)
       