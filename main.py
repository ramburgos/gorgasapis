from fastapi import FastAPI,Depends
from sqlalchemy import and_, or_ ,select,insert,update,delete,join
from sqlalchemy.orm import Session
import bcrypt 
import random
import string
import datetime
from pydantic import BaseModel
from gorgasmodels import pagolicencia_choices, tipolicencia_choices,  pagovacacion_choices, quincenas_choices,meses_choices, MotiveLicense, AppUser,Employees,BloodType,CivilStatus,ScholarShip,MotivePermission,Permissions,Licenses,Vacations,Journeys,Compensatories
from database import get_db
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI(title="APIs-SIGORGAS",
             version="1.0.0",
             openapi_url="/openapi.json",
             docs_url = "/docs",
             )

app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ItemPermission(BaseModel):
    employee_id:int
    contracts_id:int
    motivepermission_id:int
    observacion:str
    fechadesde:datetime.date
    horadesde:datetime.time
    fechahasta:datetime.date
    horahasta:datetime.time
    horastomadas:str
    estado:int
    created_by:str
    created_at:datetime.datetime

class ItemVacations(BaseModel):
    employee_id:int
    contracts_id:int
    observacion:str
    tomardesde:datetime.date
    tomarhasta:datetime.date
    fechareintegrosolicitud:datetime.date
    diasatomar:int
    diastomados:int
    proporcional:int
    pagovacacion:pagovacacion_choices
    quincenapagovacacion:quincenas_choices
    mespagovacacion:meses_choices
    anopagovacacion:int
    estado:int
    created_by:str
    created_at:datetime.datetime
   
class ItemLicenses(BaseModel):
    employee_id:int
    contracts_id:int
    tipo:tipolicencia_choices
    motivelicense_id:int
    fechadesde:datetime.date
    fechahasta:datetime.date
    diasportomar:int
    documentocss:str
    pagolicencia: pagolicencia_choices
    nombrebanco:str
    cuentabancaria:str
    estado:int
    created_by:str
    created_at:datetime.datetime
    
class ItemJourneys(BaseModel):
    employee_id:int
    contracts_id:int
    observacion:str
    fechadesde:datetime.date
    fechahasta:datetime.date
    horaspreviasentrada:int
    estado:int
    created_by:str
    created_at:datetime.datetime

class ItemCompensatories(BaseModel):
    employee_id:int
    contracts_id:int
    observacion:str
    fechadesde:datetime.date
    horadesde:datetime.time
    fechahasta:datetime.date
    horahasta:datetime.time
    horastotales:str
    estado:int
    created_by:str
    created_at:datetime.datetime
    
@app.post("/")
async def root():
    return

@app.get("/")
async def root():
    return

##################### verificación de correo electronico
@app.get("/verificarcorreo/{email}", description="Verificar Correo Usuario para poder registralo")
async def verificarcorreo (email:str, db: Session = Depends(get_db)):
    empleado_query= db.query(Employees).filter( or_(Employees.email==email, Employees.email_inst==email)).first()
    if empleado_query:
        return {"estado":"Success", "mensaje":"El correo está registrado", "data":empleado_query}
    else:
        return {"estado":"Failed", "mensaje": "El correo no esta registrado"}

##################### verificación existencia de usuario    
@app.get("/verificarusuario/{idempleado}", description="Verificar Usuario para poder agregarlo")
async def verificarusuario (idempleado:int,db: Session = Depends(get_db)):
    usuario_query= db.query(AppUser).filter_by(employee_id=idempleado).first()
    if usuario_query:
        return {"estado":"Success", "mensaje":"El usuario fue registrado con anterioridad", "data":usuario_query}
    else:
        return {"estado":"Failed", "mensaje":"El usuario no esta registrado"}
    
##################### enviardatossmtp    
@app.get("/datossmtp", description="enviar datos smtp")
async def datossmtp():
    datos = {"smtp_server":"smtp.gmail.com","sender_email": "notificaciones@gorgas.gob.pa","password": "nlkfxgmqqmzlhsot",}
           # return {"estado":"Success","mensaje":"Bienvenido "+ result[1] + ' ' + result[2], "datos":datos}
    return {"estado":"Success", "mensaje":"Datos SMTP","data":datos}
    
    

#################### registrar usuario y asignar password    
@app.post("/registrarusuario/{idempleado}", description="Agregar o Registrar Usuario y enviar correo con su nueva contraseña")
async def registrarusuario (idempleado:int,db: Session = Depends(get_db)):
    all_character= string.ascii_letters+string.digits+string.ascii_uppercase
    largopassword=6
    passwordrandom= ''.join(random.choices(all_character,k=largopassword)).encode('utf8')
    print(passwordrandom)
    hashed= bcrypt.hashpw(passwordrandom, bcrypt.gensalt())
    query = insert(AppUser).values(password=str(hashed.decode('utf-8')),estado=0,employee_id=idempleado)
    usuario_query= db.execute(query)
    db.commit() 
    if usuario_query:
        datos = {"new_password": passwordrandom}
        return {"estado":"Success", "mensaje":"El usuario se ha registrado correctamente","data":datos}
    else:
        return {"estado":"Failed", "mensaje":"El usuario no se pudo registrar correctamente"}


#######################################################################################################################
########################## VALIDAR USUARIO PARA INICIAR SESION
##########################

@app.get("/validarusuario/{email}/{password}", description="Validación de Usuario")
async def validarusuario (email:str,password:str,db: Session = Depends(get_db)):
    query = db.execute(select(AppUser.id, AppUser.employee_id, Employees.nombre1, Employees.apellido1,AppUser.password,Employees.foto).join(Employees,AppUser.employee_id == Employees.employee_id).where(or_(Employees.email == email, Employees.email_inst == email))).first()
    if not query:
        return {"estado":"Failed","mensaje":"Las credenciales son inválidas"}    
    else:
        result= query._data
        hashed_password = result[4]
        if not bcrypt.checkpw(password.encode(),hashed_password.encode()):
            return {"estado":"Failed","mensaje":"Contraseña Inválida"}
        else:
            datos = {"id_user":result[0],"id_empleado":result[1],"nombre": result[2],"apellido": result[3],"foto": result[5]}
            return {"estado":"Success","mensaje":"Bienvenido "+ result[2] + ' ' + result[3], "datos":datos}

########################## obtener generales ############################################
@app.get("/perfil/{idempleado}", description="Datos de perfil del empleado")
async def perfil (idempleado:int,db: Session = Depends(get_db)):
    subqueryescolaridad=select(ScholarShip.descripcion).where(Employees.scholarship_id == ScholarShip.scholarship_id).scalar_subquery()
    subquerytiposangre=select(BloodType.descripcion).where(Employees.bloodtype_id == BloodType.bloodtype_id).scalar_subquery()
    subqueryestadocivil=select(CivilStatus.descripcion).where(Employees.civilstatus_id == CivilStatus.civilstatus_id).scalar_subquery()
    query=  db.execute(select(AppUser.employee_id, Employees.cedula,Employees.nombre1, Employees.apellido1,Employees.direccion,Employees.direccionsecundaria,subqueryescolaridad.label("escolaridad"),subquerytiposangre.label("tiposangre"), subqueryestadocivil.label("estadocivil"),Employees.profesion).join(Employees,AppUser.employee_id == Employees.employee_id).where(Employees.employee_id == idempleado)).first()
    if not query:
        return {"estado":"Failed", "mensaje":"Request de datos de Empleado no exitoso"}
    else:
        result= query._data
        datos = {"id":result[0],"cedula":result[1],"nombre": result[2],"apellido": result[3],"direccion": result[4],"direccionsecundaria": result[5],"escolaridad": result[6],"tiposangre": result[7],"estadocivil": result[8],"profesion": result[9]}  
        return {"estado":"Success", "mensaje":"Request de Datos de Empleado exitoso", "data":datos}
       

########################## obtener generales ############################################
@app.get("/empleados/", description="Mostrar todos los empleados")
async def empleados (db: Session = Depends(get_db)):
    #subqueryescolaridad=select(ScholarShip.descripcion).where(Employees.scholarship_id == ScholarShip.scholarship_id).scalar_subquery()
    #subquerytiposangre=select(BloodType.descripcion).where(Employees.bloodtype_id == BloodType.bloodtype_id).scalar_subquery()
    #subqueryestadocivil=select(CivilStatus.descripcion).where(Employees.civilstatus_id == CivilStatus.civilstatus_id).scalar_subquery()
    query=  db.execute(select(Employees.employee_id, Employees.cedula,Employees.nombre1, Employees.apellido1,Employees.direccion,Employees.direccionsecundaria,Employees.profesion)).all()
    if not query:
        return {"estado":"Failed", "mensaje":"Request de Empleados no exitoso"}
    else:
        datos=[{"id":item[0],"cedula":item[1],"nombre": item[2],"apellido": item[3],"direccion": item[4],"direccionsecundaria": item[5],"profesion": item[6]} for item in query]
        return {"estado":"Success", "mensaje":"Request de Empleado exitoso", "datos":datos}

########################################################################################################################################
########################## CONTRATOS O TOMAS DE POSESION
##########################



     
#########################################################################################################################################
########################### MARCACIONES HISTORIAL
###########################
@app.get("/marcaciones/historial/{idempleado}/{desde}/{hasta}", description="Historial de Marcaciones")
async def marcaciones_historial (idempleado:int,desde:str,hasta:str, db:Session = Depends(get_db)):
    query = db.execute(select(AppUser.employee_id,Employees.nombre1,Employees.apellido1,AppUser.password).join(Employees,AppUser.employee_id == Employees.employee_id).where(or_(Employees.email == email, Employees.email_inst == email))).first()
    #if not query:
    #    return {"estado":"Failed","mensaje":"Usuario Inválido"}    
#    else:
#        result= query._data
#        hashed_password = result[3]
#        if not bcrypt.checkpw(password.encode(),hashed_password.encode()):
#            return {"estado":"Failed","mensaje":"Password Inválido"}
#        else:
#            datos = {"id":result[0],"nombre": result[1],"apellido": result[2],}
#            return {"estado":"Success","mensaje":"Usuario Válido", "datos":datos}
    return {"estado":"Success","mensaje":"En Construccion"}


#############################################################################################################################################
########################### PERMISOS HISTORIAL 
###########################
@app.get("/permisos/historial/{idempleado}", description="Historial de Permisos")
async def permisos_historial (idempleado:int, db: Session = Depends(get_db)):
    subquerymotivo=select(MotivePermission.descripcion).where(Permissions.motivepermission_id == MotivePermission.motivepermission_id).scalar_subquery()
    query=  db.execute(select(Permissions.permissions_id,Permissions.employee_id, Permissions.fechadesde, Permissions.horadesde, Permissions.fechahasta, Permissions.horahasta, Permissions.horastomadas,subquerymotivo.label("motivo")).where(Permissions.employee_id == idempleado)).all()
    if not query:
        return {"estado":"Failed", "mensaje":"No tiene permisos registrados"}
    else:
        datos=[{"id_permiso":item[0],"idempleado":item[1],"fechadesde":item[2],"horadesde": item[3],"fechahasta": item[4],"horahasta": item[5],"horastomadas": item[6],"motivo": item[7]} for item in query]
        return {"estado":"Success", "mensaje":"Mostrando permisos del empleado", "datos":datos}

###########################    
########################### PERMISOS GUARDAR
########################### 
@app.post("/permisos/guardar/", description="Guardar Permiso")
async def permisos_guardar (item:ItemPermission, db: Session = Depends(get_db)):
    query =db.execute(insert(Permissions).values(employee_id=item.employee_id,
                        contracts_id=item.contracts_id,
                        motivepermission_id=item.motivepermission_id,
                        observacion=item.observacion,
                        fechadesde=item.fechadesde,
                        horadesde=item.horadesde,
                        fechahasta=item.fechahasta,
                        horahasta=item.horahasta,
                        horastomadas=item.horastomadas,
                        estado=item.estado,
                        created_by=item.created_by,
                        created_at=item.created_at,
                        )
                    )
    db.commit() 
    if query:
        return {"estado":"Success", "mensaje":"Registro de Permiso guardado"}
    else:
        return {"estado":"Failed", "mensaje":"Registro de Permiso no guardado"}
    
###########################
########################### PERMISOS EDITAR
###########################
@app.post("/permisos/editar/{idpermiso}", description="Editar permiso")
async def permisos_editar (idpermiso:int):
    return {"estado":"Success","mensaje":"En Construccion"}
    
###########################
########################### PERMISOS EDITAR
###########################
@app.post("/permisos/eliminar/{idpermiso}", description="Eliminar permiso")
async def permisos_eliminar (idpermiso:int):
    return {"estado":"Success","mensaje":"En Construccion"}

###########################
########################### PERMISOS ADJUNTAR
###########################
@app.post("/permisos/adjuntar/{idpermiso}", description="Adjuntar archivos a permiso")
async def permisos_adjuntar (idpermiso:int):
    return {"estado":"Success","mensaje":"En Construccion"}
    
###########################
########################### PERMISOS IMPRIMIR
###########################
@app.post("/permisos/imprimir/{idpermiso}", description="Impresión de permiso")
async def permisos_imprimir (idpermiso:int):
    return {"estado":"Success","mensaje":"En Construccion"}
    

#################################################################################################################################
########################### VACACIONES HISTORIAL 
###########################
@app.get("/vacaciones/historial/{idempleado}", description="Historial de vacaciones")
async def vacaciones_historial (idempleado:int, db: Session = Depends(get_db)):
    query=  db.execute(select(Vacations.vacations_id,Vacations.employee_id, Vacations.tomardesde, Vacations.tomarhasta,Vacations.fechareintegrosolicitud,Vacations.diasatomar,Vacations.pagovacacion).where(Vacations.employee_id == idempleado)).all()
    if not query:
        return {"estado":"Failed", "mensaje":"No tiene vacaciones registradas"}
    else:
        datos=[{"id_vacaciones":item[0], "idempleado":item[1],"tomardesde":item[2],"tomarhasta": item[3],"fechareintegro": item[4],"diasatomar": item[5],"formapago": item[6].name.replace("_"," ")} for item in query]
        return {"estado":"Success", "mensaje":"Mostrando vacaciones del empleado", "datos":datos}

###########################    
########################### VACACIONES GUARDAR 
###########################
@app.post("/vacaciones/guardar/", description="Guardar Vacaciones")
async def vacaciones_guardar (item:ItemVacations, db: Session = Depends(get_db)):
    query =db.execute(insert(Vacations).values(employee_id=item.employee_id,
                        contracts_id=item.contracts_id,
                        observacion=item.observacion,
                        tomardesde=item.tomardesde,
                        tomarhasta=item.tomarhasta,
                        fechareintegrosolicitud=item.fechareintegrosolicitud,
                        diasatomar=item.diasatomar,
                        diastomados=item.diastomados,
                        pagovacacion=item.pagovacacion,
                        quincenapagovacacion=item.quincenapagovacacion,
                        mespagovacacion=item.mespagovacacion,
                        anopagovacacion=item.anopagovacacion,
                        estado=item.estado,
                        proporcional=item.proporcional,
                        created_by=item.created_by,
                        created_at=item.created_at,
                        )
                    )
    db.commit() 
    if query:
        return {"estado":"Success", "mensaje":"Registro Vacaciones guardado."}
    else:
        return {"estado":"Failed", "mensaje":"Retistro Vacaciones no guardado."}
    

#################################################################################################################################
########################### LICENCIAS HISTORIAL 
###########################
@app.get("/licencias/historial/{idempleado}", description="Historial de licencias")
async def licencias_historial (idempleado:int, db: Session = Depends(get_db)):
    subquerymotivo=select(MotiveLicense.descripcion).where(Licenses.motivelicense_id == MotiveLicense.motivelicense_id).scalar_subquery()
    query=  db.execute(select(Licenses.licenses_id,Licenses.employee_id, Licenses.fechadesde,Licenses.fechahasta,Licenses.diasportomar,Licenses.tipo,subquerymotivo.label("motivo"), Licenses.pagolicencia).where(Licenses.employee_id == idempleado)).all()
    if not query:
        return {"estado":"Failed", "mensaje":"No tiene licencias registradas"}
    else:
        datos=[{"id_licencia":item[0],"idempleado":item[1],"tomardesde":item[2],"tomarhasta": item[3],"diasportomar": item[4],"tipolicencia": item[5].name.replace("_"," "),"motivolicencia": item[6],"formapago": item[7].name.replace("_"," ")} for item in query]
        return {"estado":"Success", "mensaje":"Mostrando licencias del empleado", "datos":datos}

###########################    
########################### LICENCIAS GUARDAR 
###########################
@app.post("/licencias/guardar/", description="Guardar Licencias")
async def licencias_guardar (item:ItemLicenses, db: Session = Depends(get_db)):
    query =db.execute(insert(Licenses).values(employee_id=item.employee_id,
                        contracts_id=item.contracts_id,
                        tipo= item.tipo,
                        motivelicense_id = item.motivelicense_id,
                        fechadesde=item.fechadesde,
                        fechahasta=item.fechahasta,
                        diasportomar = item.diasportomar,
                        documentocss= item.documentocss,
                        pagolicencia=item.pagolicencia,
                        nombrebanco=item.nombrebanco,
                        cuentabancaria=item.cuentabancaria,
                        estado=item.estado,
                        created_by=item.created_by,
                        created_at=item.created_at,
                        )
                    )
    db.commit() 
    if query:
        return {"estado":"Success", "mensaje":"Registro Licencia guardado."}
    else:
        return {"estado":"Failed", "mensaje":"Retistro Licencia no guardado."}

#################################################################################################################################
########################### JORNADAS HISTORIAL 
###########################
@app.get("/jornadas/historial/{idempleado}", description="Historial de Jornadas")
async def jornadas_historial (idempleado:int, db: Session = Depends(get_db)):
    query=  db.execute(select(Journeys.journeys_id,Journeys.employee_id, Journeys.fechadesde, Journeys.fechahasta, Journeys.horaspreviasentrada, Journeys.observacion).where(Journeys.employee_id == idempleado)).all()
    if not query:
        return {"estado":"Failed", "mensaje":"No tiene J. Extraordinarias registradas"}
    else:
        datos=[{"id_jornada":item[0],"idempleado":item[1],"fechadesde":item[2],"fechahasta": item[3],"horaspreviasentrada": item[4],"observacion": str(item[5][0:50] + "...")} for item in query]
        return {"estado":"Success", "mensaje":"Mostrando J. Extraordinarias del empleado", "datos":datos}

###########################    
########################### JORNADAS GUARDAR 
###########################
@app.post("/jornadas/guardar/", description="Guardar Jornadas")
async def jornadas_guardar (item:ItemJourneys, db: Session = Depends(get_db)):
    query =db.execute(insert(Journeys).values(employee_id=item.employee_id,
                        contracts_id=item.contracts_id,
                        observacion= item.observacion,
                        fechadesde=item.fechadesde,
                        fechahasta=item.fechahasta,
                        horaspreviasentrada= item.horaspreviasentrada,
                        estado=item.estado,
                        created_by=item.created_by,
                        created_at=item.created_at,
                        )
                    )
    db.commit() 
    if query:
        return {"estado":"Success", "mensaje":"Registro J. Extraordinaria guardado."}
    else:
        return {"estado":"Failed", "mensaje":"Retistro J. Extraordinaria no guardado."}
    
#################################################################################################################################
########################### COMPENSATORIOS HISTORIAL 
###########################
@app.get("/compensatorios/historial/{idempleado}", description="Historial de Compensatorios")
async def compensatorios_historial (idempleado:int, db: Session = Depends(get_db)):
    query=  db.execute(select(Compensatories.compensatories_id,Compensatories.employee_id, Compensatories.fechadesde,Compensatories.horadesde,Compensatories.fechahasta, Compensatories.horahasta,Compensatories.horastotales).where(Compensatories.employee_id == idempleado)).all()
    if not query:
        return {"estado":"Failed", "mensaje":"No tiene T. Compensatorios registradas"}
    else:
        datos=[{"id_compensatorio":item[0],"idempleado":item[1],"fechadesde":item[2],"horadesde": item[3],"fechahasta": item[4],"horahasta": item[5],"horastotales": item[6]} for item in query]
        return {"estado":"Success", "mensaje":"Mostrando T. Compensatorios del empleado", "datos":datos}

###########################    
########################### COMPENSATORIOS GUARDAR 
###########################
@app.post("/compensatorios/guardar/", description="Guardar Compensatorios")
async def compensatorios_guardar (item:ItemCompensatories, db: Session = Depends(get_db)):
    query =db.execute(insert(Compensatories).values(employee_id=item.employee_id,
                        contracts_id=item.contracts_id,
                        observacion=item.observacion,
                        fechadesde=item.fechadesde,
                        horadesde=item.horadesde,
                        fechahasta=item.fechahasta,
                        horahasta=item.horahasta,
                        horastotales= item.horastotales,
                        estado=item.estado,
                        created_by=item.created_by,
                        created_at=item.created_at,
                        )
                    )
    db.commit() 
    if query:
        return {"estado":"Success", "mensaje":"Registro T. Compensatorio guardado."}
    else:
        return {"estado":"Failed", "mensaje":"Retistro T. Compensatorio no guardado."}
    

            