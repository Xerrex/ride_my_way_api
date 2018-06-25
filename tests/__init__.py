from unittest import TestCase

class TestBase(TestCase):
    """Adds Http Status code testing methods
    """

    
    @staticmethod
    def assert200(response):
        """Assert that request response's status code is 200

        http_status code 200 = OK
        :param response:
        :return boolean:
        """
        assert response.status_code == 200

    @staticmethod
    def assert201(response):
        """Assert that request response's status code is 201

        http_status code 201 = CREATED
        :param response:
        :return boolean:
        """

        assert response.status_code == 201

    @staticmethod
    def assert204(response):
        """Assert that request response's status code is 201

        http_status code 204 = NO CONTENT
        :param response:
        :return bool:
        """

        assert response.status_code == 204

    @staticmethod
    def assert400(response):
        """Assert that request response is status code is 400

        http_status code 400 = BAD REQUEST
        :param response:
        :return boolean:
        """
        assert response.status_code == 400

    @staticmethod
    def assert401(response):
        """Assert that request response is status code is 401

         http_status code 401 = UNAUTHORIZED
        :param response:
        :return boolean:
        """
        assert response.status_code == 401

    @staticmethod
    def assert403(response):
        """Assert that request response is status code is 403

        http_status code 403 = FORBIDDEN
        :param response:
        :return:
        """

        assert response.status_code == 403

    @staticmethod
    def assert404(response):
        """Assert that request response is status code is 404

         http_status code 404 = NOT FOUND
        :param response:
        :return boolean:
        """
        assert response.status_code == 404

    @staticmethod
    def assert409(response):
        """Assert that request response's status code is 409

        http_status code  409 = CONFLICT
        :param response:
        :return bool:
        """
        assert response.status_code == 409
        