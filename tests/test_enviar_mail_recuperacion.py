import mock


def test_invalid_email(client, user3):
    response = client.post(
        '/send_email_password_recover',
        data={
            "email": "InvalidEMail@hotmail.com"
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': "Email doesn't exist in database"}


def test_valid_email(client, user4):
    with mock.patch("yagmail.SMTP"):
        response = client.post(
            '/send_email_password_recover',
            data={
                "email": "test_gran_soldador@hotmail.com"
            }
        )
    assert response.status_code == 200
    assert response.json() == {'detail': "Checkout your email " +
                               "for password recover."}
