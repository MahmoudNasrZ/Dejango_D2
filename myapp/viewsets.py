from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from myapp.models import School,Classes
from django.core.serializers import serialize

import json
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name="dispatch")
class SchoolViewSet(View):
    def get(self, request, *args, **kwargs):
        schools = School.objects.all()
        if not schools.exists():
            return JsonResponse({"message": "No schools found"}, status=404)
        
        schools_json = [
        {
            "id": school.id,
            "name": school.name,
            "number_of_classes": school.number_of_classes,
            "computed_area": school.computed_area,
        }
        for school in schools
    ]
        print(schools_json)
        context = {"schools":schools_json}

        return render(request, "school.html",context)

    def post(self, request, *args, **kwargs):
        try:
            # Check if data is JSON or Form Data
            if request.content_type == "application/json":
                data = json.loads(request.body.decode("utf-8"))
            else:
                data = request.POST.dict()  # Convert form data to dictionary

            logger.debug(f"Received Data: {data}")  # Debugging

            # Ensure required fields are present
            if not all(k in data for k in ["name", "number_of_classes", "area"]):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Create and save school
            school = School(name=data["name"], number_of_classes=int(data["number_of_classes"]))
            school.set_area(data["area"])
            school.save()
            
            logger.debug(f"Saved School: {school}")  # Debugging
            return redirect("school_list")

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
    def put(self, request, school_id):
        """Update an existing school's details (full update)."""
        try:
            data = json.loads(request.body.decode("utf-8"))
            school = School.objects.get(id=school_id)

            school.name = data.get("name", school.name)
            school.number_of_classes = int(data.get("number_of_classes", school.number_of_classes))
            school.set_area(data.get("area", f"{school.computed_area}"))  # Keep old area if not provided
            school.save()

            return JsonResponse({"message": "School updated successfully"})

        except School.DoesNotExist:
            return JsonResponse({"error": "School not found"}, status=404)
        except (json.JSONDecodeError, ValueError) as e:
            return JsonResponse({"error": str(e)}, status=400)

    def patch(self, request, school_id):
        """Partial update of school details."""
        try:
            data = json.loads(request.body.decode("utf-8"))
            school = School.objects.get(id=school_id)

            if "name" in data:
                school.name = data["name"]
            if "number_of_classes" in data:
                school.number_of_classes = int(data["number_of_classes"])
            if "area" in data:
                school.set_area(data["area"])

            school.save()
            return JsonResponse({"message": "School partially updated successfully"})

        except School.DoesNotExist:
            return JsonResponse({"error": "School not found"}, status=404)
        except (json.JSONDecodeError, ValueError) as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, school_id):
        """Delete a school."""
        try:
            school = School.objects.get(id=school_id)
            school.delete()
            return JsonResponse({"message": "School deleted successfully"})

        except School.DoesNotExist:
            return JsonResponse({"error": "School not found"}, status=404)


@method_decorator(csrf_exempt, name="dispatch")
class ClassesViewSet(View):
    def get(self, request, *args, **kwargs):
        """Retrieve all classes as JSON."""
        classes = Classes.objects.all()
        if not classes.exists():
            return JsonResponse({"message": "No classes found"}, status=404)
        
        classes_json = [
            {
                "id": class_obj.id,
                "school": class_obj.school.id if class_obj.school else None,
                "class": class_obj.name,
                "computed_area": float(class_obj.computed_area) if class_obj.computed_area else None,
            }
            for class_obj in classes
        ]
        print(classes_json)
        return render(request, "classes.html",{"classes": classes_json})
    def post(self, request, *args, **kwargs):
            try:
                if request.content_type == "application/json":
                    data = json.loads(request.body.decode("utf-8"))
                else:
                    data = request.POST.dict()

                logger.debug(f"Received Data: {data}")

                # Validate required fields
                missing_fields = [k for k in ["class_name", "school_id", "area"] if k not in data]
                if missing_fields:
                    return JsonResponse({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

                # Validate School ID
                try:
                    school = School.objects.get(id=int(data["school_id"]))
                except (School.DoesNotExist, ValueError):
                    return JsonResponse({"error": "Invalid or missing school ID"}, status=404)

                # Create and save the class
                class_obj = Classes(school=school, name=data["class_name"])
                class_obj.set_area(data["area"])  # Set area before saving
                class_obj.save()

                return JsonResponse({"message": "Class created successfully!", "class_id": class_obj.id}, status=201)

            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)
            
    def put(self, request, class_id, *args, **kwargs):
        """Update an existing class."""
        try:
            class_obj = Classes.objects.get(id=class_id)
        except Classes.DoesNotExist:
            return JsonResponse({"error": "Class not found"}, status=404)

        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        # Update class name if provided
        if "name" in data:
            class_obj.name = data["name"]

        # Validate and update school ID
        if "school_id" in data:
            try:
                class_obj.school = School.objects.get(id=int(data["school_id"]))
            except School.DoesNotExist:
                return JsonResponse({"error": "Invalid school ID"}, status=400)

        # Update area if provided
        if "area" in data:
            try:
                class_obj.set_area(data["area"])
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)

        class_obj.save()
        return JsonResponse({"message": "Class updated successfully"}, status=200)

    def patch(self, request, class_id):
        """Partial update of class details."""
        try:
            data = json.loads(request.body.decode("utf-8"))
            class_obj = Classes.objects.get(id=class_id)

            if "name" in data:
                class_obj.name = data["name"]
            if "school_id" in data:
                class_obj.school = School.objects.get(id=int(data["school_id"]))
            if "area" in data:
                class_obj.set_area(data["area"])

            class_obj.save()
            return JsonResponse({"message": "Class partially updated successfully"})

        except Classes.DoesNotExist:
            return JsonResponse({"error": "Class not found"}, status=404)
        except School.DoesNotExist:
            return JsonResponse({"error": "Invalid school ID"}, status=400)
        except (json.JSONDecodeError, ValueError) as e:
            return JsonResponse({"error": str(e)}, status=400)

    def delete(self, request, class_id):
        """Delete a class."""
        try:
            class_obj = Classes.objects.get(id=class_id)
            class_obj.delete()
            return JsonResponse({"message": "Class deleted successfully"})

        except Classes.DoesNotExist:
            return JsonResponse({"error": "Class not found"}, status=404)
