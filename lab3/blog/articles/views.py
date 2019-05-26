from django.shortcuts import render, redirect
from blog.articles.models import Article
from django.http import Http404

def archive(request):
    return render(request, "archive.html", {"posts": Article.objects.all()})


def get_article(request, id):
    try:
        post = Article.objects.filter(id=id)
        return render(request, 'article.html', {"posts": post})
    except Article.DoesNotExist:
        raise Http404


def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            form = {
                'text': request.POST["text"],
                'title': request.POST["title"]
            }
            if form["text"] and form["title"]:
                if len(Article.objects.filter(title=form['title'])) > 0:
                    raise Http404
                else:
                    Article.objects.create(text=form["text"],
                                           title=form["title"],
                                           author=request.user)
                    article = Article.objects.get(title=form['title'])
                    return redirect('get_article', article.id)
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:

            return render(request, 'create_post.html', {})
    else:
        raise Http404
