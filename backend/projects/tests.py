from django.urls import reverse
from django.contrib.auth import get_user_model

import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import *

User = get_user_model()


class ProjectTests(APITestCase):

    def setUp(self):
        user_test1 = User.objects.create_user(username="test1", password="1q2w3e", first_name="test1",
                                              last_name="test1", email="test1@email.com")
        user_test2 = User.objects.create_user(username="test2", password="1q2w3e4r5t", first_name="test2",
                                              last_name="test2", email="test2@email.com")
        user_test1.save()
        user_test2.save()

        self.project1 = Project.objects.create(
            manager=user_test1,
            project_name="TestProject1"
        )

        self.project2 = Project.objects.create(
            manager=user_test2,
            project_name="TestProject2"
        )

        self.data = {
            "project_name": "TestProject3"
        }
        self.data_invalid = {
            "project_name": ""
        }
        self.data_patch = {
            "project_name": "TestProjectPatch"
        }

        position = Position.objects.create(title='tmp', color="#000000", project=self.project1)
        employee2 = Employee.objects.create(user=user_test2, position=position, project=self.project1)  # user2 - employee в project1

        self.user1_token = Token.objects.create(user=user_test1)
        self.user2_token = Token.objects.create(user=user_test2)

    # GET
    def test_unauthorized_manager_projects(self):  # Созданные проекты без авторизации
        response = self.client.get(reverse('list_my_projects'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_manager_projects(self):  # Созданные проекты
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('list_my_projects'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0].get('project_name'), 'TestProject1')

    # POST
    def test_create_projects(self):  # Создание проекта
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.post(reverse('list_my_projects'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_projects(self):  # Invalid data в создании проекта
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.post(reverse('list_my_projects'), self.data_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthorized_create_projects(self):  # Не авторизованное создание проекта
        response = self.client.post(reverse('list_my_projects'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('detail'), 'Unauthorized')

    # GET
    def test_participant_projects(self):  # Проекты юзер-участник
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.get(reverse('list_part_projects'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0].get('project_name'), 'TestProject1')

    def test_unauthorized_participant_projects(self):  # Не авторизованный юзер-участник
        response = self.client.get(reverse('list_part_projects'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('detail'), 'Unauthorized')

    # GET
    def test_get_project(self):  # Проект по id
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.get(reverse('project_id', args=[self.project2.id]), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('project_name'), 'TestProject2')

    def test_unauthorized_get_project(self):  # Не авторизованный get проекта по id
        response = self.client.get(reverse('project_id', args=[self.project2.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get('detail'), 'Учетные данные не были предоставлены.')

    def test_notManager_get_project(self):  # Не создательно get проекта по id
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.get(reverse('project_id', args=[self.project2.id]), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('project_name'), 'TestProject2')

    # PATCH
    def test_patch_project(self):  # Изменения проекта
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.patch(reverse('project_id', args=[self.project2.id]), self.data_patch, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('project_name'), 'TestProjectPatch')

    def test_notManager_patch_project(self):  # Изменение проекта не создателем
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.patch(reverse('project_id', args=[self.project2.id]), self.data_patch, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_patch_project(self):  # Инвалидная дата для изменения
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.patch(reverse('project_id', args=[self.project2.id]), self.data_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # DELETE
    def test_delete_project(self):  # Удаление проекта
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.delete(reverse('project_id', args=[self.project2.id]), format='json')
        self.assertEqual(response.status_code, 200)

    def test_notManager_delete_project(self):  # Удаление проекта не создателем
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.delete(reverse('project_id', args=[self.project2.id]), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PositionTests(APITestCase):

    def setUp(self):
        user_test1 = User.objects.create_user(username="test1", password="1q2w3e", first_name="test1",
                                              last_name="test1", email="test1@email.com")
        user_test1.save()
        user_test2 = User.objects.create_user(username="test2", password="1q2w3e4r5t", first_name="test2",
                                              last_name="test2", email="test2@email.com")
        user_test2.save()

        self.project1 = Project.objects.create(
            manager=user_test1,
            project_name="TestProject1"
        )

        self.data = {
            "title": "TestPosition",
            "color": "#010101",
            "project": self.project1.id
        }
        self.data_invalid = {
            "title": "",
            "color": "#010101",
            "project": self.project1.id
        }
        self.data_patch = {
            "title": "TestPositionPatch",
            "color": "#010101",
            "project": self.project1.id
        }
        self.user1_token = Token.objects.create(user=user_test1)
        self.user2_token = Token.objects.create(user=user_test2)
        self.position = Position.objects.create(title='testPos', color="#000000", project=self.project1)

    # GET
    def test_get_positions(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('project_positions_list', args=[self.project1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0].get('title'), 'testPos')

    def test_unAuth_get_positions(self):
        response = self.client.get(reverse('project_positions_list', args=[self.project1.id]))
        self.assertEqual(response.status_code, 401)

    def test_notPart_get_positions(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.get(reverse('project_positions_list', args=[self.project1.id]))
        self.assertEqual(response.status_code, 403)

    # POST
    def test_unAuth_post_positions(self):
        response = self.client.post(reverse('project_positions_list', args=[self.project1.id]), self.data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_notPart_post_positions(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.post(reverse('project_positions_list', args=[self.project1.id]), self.data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_post_positions(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.post(reverse('project_positions_list', args=[self.project1.id]), self.data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('title'), 'TestPosition')

    def test_invalid_post_positions(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.post(reverse('project_positions_list', args=[self.project1.id]), self.data_invalid,
                                    format='json')
        self.assertEqual(response.status_code, 400)

    # GET
    def test_get_detail_position(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('project_positions_id', args=[self.project1.id, self.position.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), 'testPos')

    def test_unAuth_get_detail_position(self):
        response = self.client.get(reverse('project_positions_id', args=[self.project1.id, self.position.id]))
        self.assertEqual(response.status_code, 401)

    def test_notPart_get_detail_position(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.get(reverse('project_positions_id', args=[self.project1.id, self.position.id]))
        self.assertEqual(response.status_code, 403)

    # PATCH
    def test_patch_position(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.patch(reverse('project_positions_id', args=[self.project1.id, self.position.id]),
                                     self.data_patch, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('title'), 'TestPositionPatch')

    def test_unAuth_patch_position(self):
        response = self.client.patch(reverse('project_positions_id', args=[self.project1.id, self.position.id]),
                                     self.data_patch, format='json')
        self.assertEqual(response.status_code, 401)

    def test_notPart_patch_position(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.patch(reverse('project_positions_id', args=[self.project1.id, self.position.id]),
                                     self.data_patch, format='json')
        self.assertEqual(response.status_code, 403)

    def test_invalid_patch_position(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.patch(reverse('project_positions_id', args=[self.project1.id, self.position.id]),
                                     self.data_invalid, format='json')
        self.assertEqual(response.status_code, 400)

    # DELETE
    def test_delete_position(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.delete(reverse('project_positions_id', args=[self.project1.id, self.position.id]),
                                      format='json')
        self.assertEqual(response.status_code, 200)

    def test_unAuth_delete_position(self):
        response = self.client.delete(reverse('project_positions_id', args=[self.project1.id, self.position.id]),
                                      format='json')
        self.assertEqual(response.status_code, 401)

    def test_notPart_delete_position(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.delete(reverse('project_positions_id', args=[self.project1.id, self.position.id]),
                                      format='json')
        self.assertEqual(response.status_code, 403)


class TaskTypeTests(APITestCase):

    def setUp(self):
        user_test1 = User.objects.create_user(username="test1", password="1q2w3e", first_name="test1",
                                              last_name="test1", email="test1@email.com")
        user_test1.save()
        user_test2 = User.objects.create_user(username="test2", password="1q2w3e4r5t", first_name="test2",
                                              last_name="test2", email="test2@email.com")
        user_test2.save()

        self.project1 = Project.objects.create(
            manager=user_test1,
            project_name="TestProject1"
        )

        self.data = {
            "title": "TestTaskType",
            "color": "#010101",
            "project": self.project1.id
        }
        self.data_invalid = {
            "title": "",
            "color": "#010101",
            "project": self.project1.id
        }
        self.data_patch = {
            "title": "TestTaskTypePatch",
            "color": "#010101",
            "project": self.project1.id
        }
        self.user1_token = Token.objects.create(user=user_test1)
        self.user2_token = Token.objects.create(user=user_test2)
        self.taskType = TaskType.objects.create(title='testType', color="#000000", project=self.project1)

    # GET
    def test_get_taskTypes(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('project_taskType_list', args=[self.project1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0].get('title'), 'testType')

    def test_unAuth_get_taskTypes(self):
        response = self.client.get(reverse('project_taskType_list', args=[self.project1.id]))
        self.assertEqual(response.status_code, 401)

    def test_notPart_get_taskTypes(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.get(reverse('project_taskType_list', args=[self.project1.id]))
        self.assertEqual(response.status_code, 403)

    # POST
    def test_unAuth_post_taskType(self):
        response = self.client.post(reverse('project_taskType_list', args=[self.project1.id]), self.data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_notPart_post_taskType(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.post(reverse('project_taskType_list', args=[self.project1.id]), self.data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_post_taskType(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.post(reverse('project_taskType_list', args=[self.project1.id]), self.data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('title'), 'TestTaskType')

    def test_invalid_post_taskType(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.post(reverse('project_taskType_list', args=[self.project1.id]), self.data_invalid,
                                    format='json')
        self.assertEqual(response.status_code, 400)

    # GET
    def test_get_detail_taskType(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('project_taskType_id', args=[self.project1.id, self.taskType.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), 'testType')

    def test_unAuth_get_detail_taskType(self):
        response = self.client.get(reverse('project_taskType_id', args=[self.project1.id, self.taskType.id]))
        self.assertEqual(response.status_code, 401)

    def test_notPart_get_detail_taskType(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.get(reverse('project_taskType_id', args=[self.project1.id, self.taskType.id]))
        self.assertEqual(response.status_code, 403)

    # PATCH
    def test_patch_taskType(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.patch(reverse('project_taskType_id', args=[self.project1.id, self.taskType.id]),
                                     self.data_patch, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('title'), 'TestTaskTypePatch')

    def test_unAuth_patch_taskType(self):
        response = self.client.patch(reverse('project_taskType_id', args=[self.project1.id, self.taskType.id]),
                                     self.data_patch, format='json')
        self.assertEqual(response.status_code, 401)

    def test_notPart_patch_taskType(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.patch(reverse('project_taskType_id', args=[self.project1.id, self.taskType.id]),
                                     self.data_patch, format='json')
        self.assertEqual(response.status_code, 403)

    def test_invalid_patch_taskType(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.patch(reverse('project_taskType_id', args=[self.project1.id, self.taskType.id]),
                                     self.data_invalid, format='json')
        self.assertEqual(response.status_code, 400)

    # DELETE
    def test_delete_taskType(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.delete(reverse('project_taskType_id', args=[self.project1.id, self.taskType.id]),
                                      format='json')
        self.assertEqual(response.status_code, 200)

    def test_unAuth_delete_taskType(self):
        response = self.client.delete(reverse('project_taskType_id', args=[self.project1.id, self.taskType.id]),
                                      format='json')
        self.assertEqual(response.status_code, 401)

    def test_notPart_delete_taskType(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.delete(reverse('project_taskType_id', args=[self.project1.id, self.taskType.id]),
                                      format='json')
        self.assertEqual(response.status_code, 403)


class EmployeeTest(APITestCase):
    def setUp(self):
        self.user_test1 = User.objects.create_user(username="test1", password="1q2w3e", first_name="test1",
                                              last_name="test1", email="test1@email.com")
        self.user_test1.save()
        self.user_test2 = User.objects.create_user(username="test2", password="1q2w3e4r5t", first_name="test2",
                                              last_name="test2", email="test2@email.com")
        self.user_test2.save()

        self.project1 = Project.objects.create(
            manager=self.user_test1,
            project_name="TestProject1"
        )

        self.position1 = Position.objects.create(title='testPos1', color="#000000", project=self.project1)
        self.position2 = Position.objects.create(title='testPos2', color="#000000", project=self.project1)

        self.employee1 = Employee.objects.create(user=self.user_test1, position=self.position1, project=self.project1)

        self.data = {
            "user": self.user_test2.id,
            "position": self.position2.id,
            "chief": "",
            "project": self.project1.id
        }
        self.data_invalid_user = {
            "user": 234,
            "position": self.position2.id,
            "chief": "",
            "project": self.project1.id
        }
        self.data_patch = {
            "user": self.user_test2.id,
            "position": self.position1.id,
            "chief": "",
            "project": self.project1.id
        }
        self.user1_token = Token.objects.create(user=self.user_test1)
        self.user2_token = Token.objects.create(user=self.user_test2)

    # GET
    def test_get_employees(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('project_employee_list', args=[self.project1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0].get('user'), self.user_test1.id)

    def test_unAuth_get_employees(self):
        response = self.client.get(reverse('project_employee_list', args=[self.project1.id]))
        self.assertEqual(response.status_code, 401)

    def test_notPart_get_employees(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.get(reverse('project_employee_list', args=[self.project1.id]))
        self.assertEqual(response.status_code, 403)

    # POST
    def test_unAuth_post_employee(self):
        response = self.client.post(reverse('project_employee_list', args=[self.project1.id]), self.data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_notPart_post_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.post(reverse('project_employee_list', args=[self.project1.id]), self.data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_post_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.post(reverse('project_employee_list', args=[self.project1.id]), self.data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('user'), self.user_test2.id)

    def test_invalidUser_post_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.post(reverse('project_employee_list', args=[self.project1.id]), self.data_invalid_user,
                                    format='json')
        self.assertEqual(response.status_code, 400)

# GET
    def test_get_detail_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('project_employee_id', args=[self.project1.id, self.employee1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('user'), self.user_test1.id)

    def test_unAuth_get_detail_employee(self):
        response = self.client.get(reverse('project_employee_id', args=[self.project1.id, self.employee1.id]))
        self.assertEqual(response.status_code, 401)

    def test_notPart_get_detail_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.get(reverse('project_employee_id', args=[self.project1.id, self.employee1.id]))
        self.assertEqual(response.status_code, 403)

    # PATCH
    def test_patch_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.patch(reverse('project_employee_id', args=[self.project1.id, self.employee1.id]),
                                     self.data_patch, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('position'), self.position1.id)

    def test_unAuth_patch_employee(self):
        response = self.client.patch(reverse('project_employee_id', args=[self.project1.id, self.employee1.id]),
                                     self.data_patch, format='json')
        self.assertEqual(response.status_code, 401)

    def test_notPart_patch_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.patch(reverse('project_employee_id', args=[self.project1.id, self.employee1.id]),
                                     self.data_patch, format='json')
        self.assertEqual(response.status_code, 403)

    def test_invalid_patch_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.patch(reverse('project_employee_id', args=[self.project1.id, self.employee1.id]),
                                     self.data_invalid_user, format='json')
        self.assertEqual(response.status_code, 400)

    # DELETE
    def test_delete_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.delete(reverse('project_employee_id', args=[self.project1.id, self.employee1.id]),
                                      format='json')
        self.assertEqual(response.status_code, 200)

    def test_unAuth_delete_employee(self):
        response = self.client.delete(reverse('project_employee_id', args=[self.project1.id, self.employee1.id]),
                                      format='json')
        self.assertEqual(response.status_code, 401)

    def test_notPart_delete_employee(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.delete(reverse('project_employee_id', args=[self.project1.id, self.employee1.id]),
                                      format='json')
        self.assertEqual(response.status_code, 403)


class TaskTests(APITestCase):
    def setUp(self):
        self.user_test1 = User.objects.create_user(username="test1", password="1q2w3e", first_name="test1",
                                                   last_name="test1", email="test1@email.com")
        self.user_test1.save()
        self.user_test2 = User.objects.create_user(username="test2", password="1q2w3e4r5t", first_name="test2",
                                                   last_name="test2", email="test2@email.com")
        self.user_test2.save()

        self.project1 = Project.objects.create(
            manager=self.user_test1,
            project_name="TestProject1"
        )

        self.taskType1 = TaskType.objects.create(title='testPos1', color="#000000", project=self.project1)
        self.taskType2 = TaskType.objects.create(title='testPos2', color="#000000", project=self.project1)

        self.task1 = Task.objects.create(title='task1', content='task1', weight=4,
                                         dead_line="2021-11-22T00:00:00Z", is_done=False,
                                         taskType=self.taskType1, project=self.project1)

        self.data = {
            "title": "тестовая задача",
            "content": "Тестовый контент",
            "weight": 2,
            "dead_line": "2021-11-20T00:00:00Z",
            "is_done": False,
            "taskType": self.taskType2.id,
            #"doers": ""
        }
        self.data_invalid = {
            "title": "тестовая задача",
            "content": "Тестовый контент",
            "weight": 2,
            "dead_line": "2021-11-20T00:00:00Z",
            "is_done": False,
            "taskType": self.taskType2.id,
            "doers": ""
        }
        self.data_patch = {
            "title": "patch",
        }
        self.user1_token = Token.objects.create(user=self.user_test1)
        self.user2_token = Token.objects.create(user=self.user_test2)

# GET
    def test_get_tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('project_task_list', args=[self.project1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0].get('title'), "task1")

    def test_unAuth_get_tasks(self):
        response = self.client.get(reverse('project_task_list', args=[self.project1.id]))
        self.assertEqual(response.status_code, 401)

    def test_notPart_get_tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.get(reverse('project_task_list', args=[self.project1.id]))
        self.assertEqual(response.status_code, 403)


    # POST
    def test_unAuth_post_tasks(self):
        response = self.client.post(reverse('project_task_list', args=[self.project1.id]), self.data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_notPart_post_tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.post(reverse('project_task_list', args=[self.project1.id]), self.data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_post_tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.post(reverse('project_task_list', args=[self.project1.id]), self.data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('title'), 'тестовая задача')

    def test_invalid_post_tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.post(reverse('project_task_list', args=[self.project1.id]), self.data_invalid,
                                    format='json')
        self.assertEqual(response.status_code, 400)

    # GET
    def test_get_detail_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('project_task_id', args=[self.project1.id, self.task1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), "task1")

    def test_unAuth_get_detail_task(self):
        response = self.client.get(reverse('project_task_id', args=[self.project1.id, self.task1.id]))
        self.assertEqual(response.status_code, 401)

    def test_notPart_get_detail_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.get(reverse('project_task_id', args=[self.project1.id, self.task1.id]))
        self.assertEqual(response.status_code, 403)

    # PATCH
    def test_patch_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.patch(reverse('project_task_id', args=[self.project1.id, self.task1.id]),
                                     self.data_patch, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('title'), 'patch')

    def test_unAuth_patch_task(self):
        response = self.client.patch(reverse('project_task_id', args=[self.project1.id, self.task1.id]),
                                     self.data_patch, format='json')
        self.assertEqual(response.status_code, 401)

    def test_notPart_patch_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.patch(reverse('project_task_id', args=[self.project1.id, self.task1.id]),
                                     self.data_patch, format='json')
        self.assertEqual(response.status_code, 403)

    def test_invalid_patch_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.patch(reverse('project_task_id', args=[self.project1.id, self.task1.id]),
                                     self.data_invalid, format='json')
        self.assertEqual(response.status_code, 400)

    # DELETE
    def test_delete_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.delete(reverse('project_task_id', args=[self.project1.id, self.task1.id]),
                                      format='json')
        self.assertEqual(response.status_code, 200)

    def test_unAuth_delete_task(self):
        response = self.client.delete(reverse('project_task_id', args=[self.project1.id, self.task1.id]),
                                      format='json')
        self.assertEqual(response.status_code, 401)

    def test_notPart_delete_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.delete(reverse('project_task_id', args=[self.project1.id, self.task1.id]),
                                      format='json')
        self.assertEqual(response.status_code, 403)


class SetEmployeeTests(APITestCase):
    def setUp(self):
        self.user_test1 = User.objects.create_user(username="test1", password="1q2w3e", first_name="test1",
                                                   last_name="test1", email="test1@email.com")
        self.user_test1.save()
        self.user_test2 = User.objects.create_user(username="test2", password="1q2w3e4r5t", first_name="test2",
                                                   last_name="test2", email="test2@email.com")
        self.user_test2.save()
        self.user_test3 = User.objects.create_user(username="test3", password="1q2w3e4r5t", first_name="test3",
                                                   last_name="test3", email="test3@email.com")
        self.user_test3.save()

        self.project1 = Project.objects.create(
            manager=self.user_test1,
            project_name="TestProject1"
        )

        self.taskType1 = TaskType.objects.create(title='testPos1', color="#000000", project=self.project1)

        self.position1 = Position.objects.create(title='testPos1', color="#000000", project=self.project1)
        self.employee2 = Employee.objects.create(user=self.user_test2, position=self.position1, project=self.project1)
        self.employee3 = Employee.objects.create(user=self.user_test3, position=self.position1, project=self.project1)
        self.task1 = Task.objects.create(title='task1', content='task1', weight=4,
                                         dead_line="2021-11-22T00:00:00Z", is_done=False,
                                         taskType=self.taskType1, project=self.project1,
                                         )
        self.task1.doers.add(self.employee3)

        self.data = {
            "doer_id": self.employee2.id
        }
        self.data_invalid = {
            "doer_id": ""
        }
        self.data_delete = {
            "doer_id": self.employee3.id
        }
        self.user1_token = Token.objects.create(user=self.user_test1)
        self.user2_token = Token.objects.create(user=self.user_test2)

    # PATCH
    def test_patch_doers(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.patch(reverse('project_set_employee', args=[self.project1.id, self.task1.id]),
                                     self.data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('doers'), [self.employee2.id, self.employee3.id])

    def test_unAuth_patch_doers(self):
        response = self.client.patch(reverse('project_set_employee', args=[self.project1.id, self.task1.id]),
                                     self.data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_notPart_patch_doers(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.patch(reverse('project_set_employee', args=[self.project1.id, self.task1.id]),
                                     self.data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_invalid_patch_doers(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.patch(reverse('project_set_employee', args=[self.project1.id, self.task1.id]),
                                     self.data_invalid, format='json')
        self.assertEqual(response.status_code, 400)

    # DELETE
    def test_delete_doers(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.delete(reverse('project_set_employee', args=[self.project1.id, self.task1.id]),
                                      self.data_delete, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('doers'), [])

    def test_unAuth_delete_doers(self):
        response = self.client.delete(reverse('project_set_employee', args=[self.project1.id, self.task1.id]),
                                      self.data_delete, format='json')
        self.assertEqual(response.status_code, 401)

    def test_notPart_delete_doers(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.delete(reverse('project_set_employee', args=[self.project1.id, self.task1.id]),
                                      self.data_delete, format='json')
        self.assertEqual(response.status_code, 403)
