from guardian.models import Guardian
from organization.models import Organization
from ustaz.models import Ustaz


def calculate_percentage(instance: Ustaz | Organization | Guardian):
    if not instance:
        return 0

    if isinstance(instance, Ustaz):
        total = {
            "phone": 10 if instance.user.phone else 0,
            "avatar": 20 if instance.user.avatar else 0,
            "address_city": 5 if instance.address.city else 0,
            "address_area": 5 if instance.address.area else 0,
            "address_house": 5 if instance.address.house else 0,
            "birth_date": 5 if instance.birth_date else 0,
            "nid_no": 10 if instance.nid_no else 0,
            "nid_front": 10 if instance.nid_front else 0,
            "educational_certificates": (
                10 if instance.education_qualification.exists() else 0
            ),
            "training_certificates": (
                10 if instance.training_certificates.exists() else 0
            ),
            "achievement_certificates": (
                10 if instance.achievement_certificates.exists() else 0
            ),
        }

        return sum(value for _, value in total.items())

    elif isinstance(instance, Organization):
        total = {
            "phone": 10 if instance.user.phone else 0,
            "avatar": 10 if instance.user.avatar else 0,
            "address_city": 5 if instance.address.city else 0,
            "address_area": 5 if instance.address.area else 0,
            "address_house": 5 if instance.address.house else 0,
            "name": 5 if instance.name else 0,
            "email": 5 if instance.email else 0,
            "website": 5 if instance.website else 0,
            "facebook_page": 5 if instance.facebook_page else 0,
            "youtube_page": 5 if instance.youtube_page else 0,
            "head_name": 5 if instance.head_name else 0,
            "head_nid": 5 if instance.head_nid else 0,
            "head_avatar": 5 if instance.head_avatar else 0,
            "teacher_accomodation": 5 if instance.teacher_accomodation else 0,
            "meal_routine": 5 if instance.meal_routine else 0,
            "hoilday_calendar": 5 if instance.hoilday_calendar else 0,
            "rules": 5 if instance.rules else 0,
            "committee_permission": 5 if instance.committee_permission else 0,
        }

        return sum(value for _, value in total.items())
    elif isinstance(instance, Guardian):
        total = {
            "phone": 20 if instance.user.phone else 0,
            "avatar": 50 if instance.user.avatar else 0,
            "address_city": 10 if instance.address.city else 0,
            "address_area": 10 if instance.address.area else 0,
            "address_house": 10 if instance.address.house else 0,
        }

        return sum(value for _, value in total.items())
    else:
        return 0
