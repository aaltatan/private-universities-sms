from pathlib import Path

from apps.hr.models import Employee
from django.core.files import File


def run():
    images_path = Path("D:/onedrive").resolve() / "financial" / "PhotosWPU" / "Profile"

    images = {image.name.split(".")[0]: image for image in images_path.glob("*.jpg")}

    employees = Employee.objects.all()

    for employee in employees:
        if employee.fullname in images:
            employee.profile.delete()
            image = open(images[employee.fullname].as_posix(), "rb")
            file = File(image)
            employee.profile.save(f"{employee.fullname.replace(' ', '_')}.jpg", file)
            image.close()
