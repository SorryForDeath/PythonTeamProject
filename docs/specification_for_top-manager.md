## ��� 1

���� ���������� �� ����������� ����� �����������:
* "��� ������������";
* "������";
* ����������� � �����������.

����� "�����������" �������� � ���������� ����� ������ "���������":

  **����**               **���������**         **��������**
employee_id            �������������         ��������������
employee_full_name     ���                   ���� ��������������
employee_position      ���������, ����       ���������� ������
employee_login         ��� ������������      ���� ��������������
employee_passwd        ������                ������� ���� ��������������
employee_access_level  ������� �������       NULL
employee_comment       �������������� �����  NULL

���������� � ���� Login:
* ����� � ��������� ��������� �����;
* �����;
* �������: "�����", "����", "�������������";
* ������ ������ ������ ���� ������.
* ����� - 16 ��������.

������ ���������� ����������� ��������, ��� ������������ � ���� employee_passwd.

## �����������

��� ����� ������ ���� "�����/������" ��������� employee_access_level:
* NULL - ������ �� ������������, ������ � ������� ��������.
* 1 - ������� "�����������". ����� �� ������ ���������� �� ������ events, visitors � tickets; ����� �� �������������� ������� events � visitors, ������� ���������� �� ���� �����������.
* 2 - ������� "���-��������". ��� �����.

## �����������

### ������� "�����������" (�������)

���������� ������������ ������ �����������, ����:
* ���������;
* ���� ����� ������;
* ���������� ��������� � ��������� �������.

��������:
* ����������� - ����� ���������� � �����������, ������� ���������� �� ������� � �����������; � ���������� �� ������� "������", "����������".
* ������������� - ��������� ������ ��� �����������, ������� ���������� �� �������������.
* ������� - �������� ������ ��� �������, � ������� ���������� �� �������������.
* �������� - ���������� ������ �����������.

#### ������� "�����������"

����� ���������� � �����������:
* ���������;
* ��������;
* ���� ����� ������;
* ������������;
* ����� ����������;
* ������;
* ����� �������������� �����;
* ������ �����������-�������������;
* ����� ���������� �������;
* ���������� ��������� � ��������� �������.
��������:
* ������������� - ��������� ������ ��� �����������, ������� ���������� �� �������������.
* ������� - �������� ������ ��� �������, � ������� ���������� �� �������������.
* ���������� - ������� �� ������� "����������" � �������� ���������� �����������;
* ����� - ��������� � ������.

#### ������� "��������"

���������� ���� ����� events. �������������:
* ���������� ������� - ������� ��������������� ���������� ������� � tickets;
* � ����������� ������������� ������������� ���������, ����������� ������ ��� �����������.

#### ������� "�������"

���������� ������ ���������� � ����������� � ������������� �� ��������.

### ������� "����������"

������������ ����� ���� �������. ��������� ������������� ����� �� ������������.
* ���;
* ����������� �����;
* ����� ��������;

��������:
* �����������.
* ���� ����� - ����� ������ ������� ����������� � ����������� ���������� ���������� �� ��������� ������������.
* �������������.
* �������.
* ��������.

#### ������� "�����������"

���������� ������ ���������� � ������������:
* ���;
* ����������� �����;
* ����� ��������;
* ������ ������� �����������, �� ������� ���������������.

## ��������

* �������: "���", "��������� ������", "��������� �����", "��� �����������", "��� ���������.
