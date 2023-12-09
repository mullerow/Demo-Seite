from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserAccountmanagmentForm, CommentForm, ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser, UserImageModel, PostModel, IndexCommentModel, VisitorCountModel
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView

def count_visitors(request):
    visitor_count, created = VisitorCountModel.objects.get_or_create(pk=1)
    visitor_count.count += 1
    visitor_count.save()
    return visitor_count.count

def index_site(request):
    if request.method == 'GET':
        form = CommentForm()
        comments = IndexCommentModel.objects.all().order_by('-id')
        context = {
            'amount_visitors': count_visitors(request),
            'is_index_page': True,
            'form': form,
            'comments': comments
        }

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if request.user.is_authenticated:
            user = request.user
        else:
            user = CustomUser.objects.get_or_create(username='AnonymousUser')[0]

        if form.is_valid():
            comment_username = form.cleaned_data['comment_username']
            comment_it_reference = form.cleaned_data['comment_it_reference']
            comment_text = form.cleaned_data['comment_text']
            comment = form.save(commit=False)
            comment.user = user
            comment.comment_image = user.profile_image.image
            comment.save()
            comment = form.save()
            messages.success(request, 'Ihr Kommentar wurde erfolgreich erstellt')
            return redirect('index_site')
        else:
            messages.error(request, 'Das Formular wurde fehlerhaft ausgefüllt')
            return redirect('index_site')

    return render(request, 'demonstrationsite/index.html', context)

class Skill_List_View(ListView):
    template_name = 'skills.html'
    model = PostModel
    context_object_name = 'posts'

class Skill_Detail_View(DetailView):
    template_name = 'skill_details.html'
    model = PostModel
    context_object_name = 'post'

def login_user(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.error(request, 'Sie haben sich erfolgreich eingeloggt')
            return redirect('login_site')
        else:
            messages.error(request, 'Der Loginversuch war nicht erfolgreich, bitte geben Sie Ihre Login-Daten erneut ein')
            return redirect('login_site')
    else:
        return render(request, 'demonstrationsite/login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Sie haben sich ausgeloggt')
    return redirect('index_site')

def register_user(request):
    if request.method != 'POST':
        form = UserRegistrationForm()
    else:
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user_name = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=user_name, password=password)
            user = form.save()
            login(request, user)
            messages.success(request, 'Sie haben erfolgreich eine Account erstellt')
            return redirect('account_site')
        else:
            if not form.cleaned_data.get('username'):
                messages.error(request, 'Bitte einen Benutzernamen eingeben')
                # Überprüfen, ob das Passwort-Feld leer ist
            if not form.cleaned_data.get('password1'):
                messages.error(request, 'Bitte ein Passwort eingeben')
            else:
                messages.error(request, 'Bitte das Formular vollständig und nach den angegebenen Vorgaben ausfüllen')
            return redirect('registration_site')


            messages.error(request, 'Bitte das Formular vollständig und nach den angebenen Vorgaben ausfüllen')
            return redirect('registration_site')

    context = {'form': form}
    return render(request, 'demonstrationsite/register.html', context)

def account_data_change(request):
    if request.user.is_authenticated:
        user = request.user
        form = UserAccountmanagmentForm(request.POST or None, instance=request.user)
        context = {'form': form}
        if request.method == 'POST':
            image_trick = user.profile_image     # the is_valid() function delete the profile_image (dont know why) so i have to work around a little
            if form.is_valid():
                user.profile_image = image_trick
                user = form.save()
                messages.error(request, 'Ihre Accountdaten wurden erfolgreich übernommen')
            else:
                messages.error(request, 'Das Formular wurde Fehlerhaft ausgefüllt')
        else:
            context = {'form': form}
    else:
        context = {}
    return render(request, 'demonstrationsite/account.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_first_name = form.cleaned_data['sender_first_name']
            sender_last_name = form.cleaned_data['sender_last_name']
            message_subject = form.cleaned_data['message_subject']
            email_message = form.cleaned_data['email_message']
            sender_email = form.cleaned_data['sender_email']
            context = {
                'sender_first_name': sender_first_name,
                'sender_last_name': sender_last_name
            }
            send_mail(
                f'Neue Kontaktanfrage von {sender_first_name} {sender_last_name}',
                f'Betreff: {message_subject}\nNachricht: {email_message}\nE-Mail: {sender_email}',
                sender_email,
                ["mypersonalemaildelivery@gmail.com"],
                fail_silently=False,
            )
            return render(request, 'demonstrationsite/contact.html', context)

        else:
            messages.error(request, 'Ihre Nachricht konnte nicht abgesendet werden. Bitte stellen Sie sicher, das sie alle Felder korrekt ausgefüllt haben')

    return render(request, 'demonstrationsite/contact.html')

def choose_image(request):
        if request.method == 'GET':
            image_models = UserImageModel.objects.all()
            images = []
            images_id = []
            for image_model in image_models:
                images.append(image_model.image)
                images_id.append(image_model.id)
            image_data = zip(images, images_id)

            return render(request, 'demonstrationsite/profil_images.html', {'image_data': image_data})

        if request.method == 'POST':
            selected_image_id = request.POST.get('selected_image')

            try:
                selected_image_model = UserImageModel.objects.get(id=selected_image_id)
                user = CustomUser.objects.get(id=request.user.id)
                user.profile_image = selected_image_model
                user.save()
                messages.success(request, 'Bild erfolgreich übernommen')

            except:
                messages.error(request, 'Das gewählte Bild wurde nicht gefunden')

            return redirect('choose_image_site')
