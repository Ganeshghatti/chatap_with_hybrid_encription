from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .file_encription import load_keys, encrypt_file, decrypt_file
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def index(request):
    return render(request, "index.html")


def file(request):
    if request.method == "POST":
        if "file" in request.FILES:
            file = request.FILES["file"]
            file_content = file.read()

            # Encrypt the file content
            encrypted_key, encrypted_data = encrypt_file(file_content)

            # Combine the encrypted key and data into a single string for download
            combined_data = f"{encrypted_key}::{encrypted_data}"

            # Create a response with the encrypted file data
            response = HttpResponse(combined_data, content_type="text/plain")
            response["Content-Disposition"] = f'attachment; filename="{file.name}.enc"'

            return response

    # Load keys and render the file upload page
    private_key, public_key = load_keys()
    context = {
        "private_key": private_key.export_key().decode("utf-8"),
        "public_key": public_key.export_key().decode("utf-8"),
    }
    return render(request, "file.html", context)


def decrypt_file_view(request):
    if request.method == "POST":
        if "encrypted_file" in request.FILES:
            encrypted_file = request.FILES["encrypted_file"]
            encrypted_file_content = encrypted_file.read().decode("utf-8")

            # Split the encrypted content into key and data parts
            encrypted_key, encrypted_data = encrypted_file_content.split("::")

            # Decrypt the file content
            decrypted_data = decrypt_file(encrypted_key, encrypted_data)

            # Create a response with the decrypted file data
            response = HttpResponse(
                decrypted_data, content_type="application/octet-stream"
            )
            response["Content-Disposition"] = (
                f'attachment; filename="{encrypted_file.name.replace(".enc", "")}"'
            )

            return response

    # Load keys and render the decryption page
    private_key, public_key = load_keys()
    context = {
        "private_key": private_key.export_key().decode("utf-8"),
        "public_key": public_key.export_key().decode("utf-8"),
    }
    return render(request, "file.html", context)


# def decrypt_file_view(request):
    if request.method == "POST":
        encrypted_file = request.FILES["encrypted_file"]
        key_file = request.FILES["private_key"]

        # Load the private key from the uploaded file
        private_key = RSA.import_key(key_file.read())

        # Read the encrypted file content
        encrypted_content = encrypted_file.read()

        # Decrypt the file content
        cipher = PKCS1_OAEP.new(private_key)
        try:
            decrypted_content = cipher.decrypt(encrypted_content)
        except (ValueError, TypeError) as e:
            return JsonResponse(
                {"error": "Invalid private key or corrupted file"}, status=400
            )

        # Create a response with the decrypted file
        response = HttpResponse(
            decrypted_content, content_type="application/octet-stream"
        )
        response["Content-Disposition"] = (
            f'attachment; filename="{encrypted_file.name.replace(".enc", "")}"'
        )
        return response

    return JsonResponse({"error": "Invalid request"}, status=400)


def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})
