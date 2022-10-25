from db import *


def test_empty_robot_list(loggedin_client):
    with db_session:
        Usuario(nombre_usuario='pedro',
                email='pedro.lopez@mi.unc.edu.ar',
                contraseña='42787067', verificado=True)
    response = loggedin_client.get('/lista-robots',
                                   data={"username": "pedro"})
    assert response.status_code == 400
    assert response.json() == {'detail': 'No se encontraron robots'}


def test_non_empty_robot_list(loggedin_client):
    with db_session:
        u = Usuario(nombre_usuario='pedro',
                    email='pedro.lopez@mi.unc.edu.ar',
                    contraseña='42787067', verificado=True)
        Robot(nombre='rob', implementacion='hola', partidas_ganadas=0,
              partidas_jugadas=0, defectuoso=False, usuario=u)
    response = loggedin_client.get('/lista-robots', data={"username": "pedro"})
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'nombre': 'rob'}]
