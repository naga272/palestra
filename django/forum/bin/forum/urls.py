from django.contrib                     import admin
from django.urls                        import path, include, re_path
from forum_app.views                    import *


""" NON TOCCARE ASSOLUTAMENTE """
from django.conf                        import settings
from django.conf.urls.static            import static
from django.contrib.staticfiles.urls    import staticfiles_urlpatterns 
from django.views.static                import serve


# pagina che si attiva in caso di url non valido (vai in views, funzione errno_404())
error_404 = "forum.views.errno_404"


# tutte le pagine per la spiegazione dei linguaggi sono raggruppate tramite classi
# C_section, Cpp_section, JS_section e Py_section all'interno del modulo views.py

urlpatterns = [
    # NB: tutti file inseriti in media/ o static/ sono visibili dal FE
    #re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    path('',                        homepage),
    path('admin/',                  admin.site.urls),
    path('desktop/',                desktop),
    path('presentation/',           presentation),
    path('download/ppt/',           download_ppt, name='download_ppt'),
    #path('forum/',                  forum),
    #path('forum/form_forum/',       form_forum),
    #path('forum/filter/',           filter_questions),
    #path('forum/question/<str:id>', forum_domanda, name="forum_domanda"),
    #path('captcha/',                include('captcha.urls')),               # captcha per eseguire domande sul forum
    path('chatbot/ask/',            chatbot_ask),
    path('library/',                library),

    # li ordino dal linguaggio meno recente al più recente
    path('library/nasm/intro',                      Nasm_section.intro),
    # path('library/nasm/lezione/<str:num_lesson>',   Nasm_section.lesson, name="lezioni nasm"),

    path('library/c/intro/',                        C_section.intro),
    path('library/c/lezione/lez<str:num_lesson>',   C_section.lesson, name="lezioni C"),
    # librerie standard C
    path('library/c/lezione/stdio.h',               C_section.stdio),
    path('library/c/lezione/stdlib.h',              C_section.stdlib),
    path('library/c/lezione/stdint.h',              C_section.stdint),
    path('library/c/lezione/string.h',              C_section.string),
    path('library/c/lezione/time.h',                C_section.time),
    path('library/c/lezione/locale.h',              C_section.locale),
    path('library/c/lezione/unistd.h',              C_section.unistd),
    path('library/c/lezione/errno.h',               C_section.errno),
    path('library/c/lezione/stdbool.h',             C_section.stdbool),
    path('library/c/lezione/stdarg.h',              C_section.stdarg),
    path('library/c/lezione/stddef.h',              C_section.stddef),
    path('library/c/lezione/search.h',              C_section.search),
    path('library/c/lezione/types.h',               C_section.types),
    path('library/c/lezione/ctype.h',               C_section.ctype),
    path('library/c/lezione/signal.h',              C_section.signal),


    path('library/cpp/intro/',                           Cpp_section.intro),
    # path('library/cpp/lezione/lez<str:num_lesson>',      Cpp_section.lesson, name="lezioni cpp"),

    path('library/py/intro/',                            Py_section.intro),
    path('library/py/lezione/lez<str:num_lesson>',       Py_section.lesson, name="lezioni python"),
    # standard librery python
    path('library/py/lezione/os',           Py_section.os),
    path('library/py/lezione/datetime',     Py_section.datetime),
    #path('library/py/lezione/sys',          Py_section.sys),
    #path('library/py/lezione/re',           Py_section.re),
    path('library/py/lezione/random',       Py_section.random),
    #path('library/py/lezione/urllib',       Py_section.urllib),
    #path('library/py/lezione/csv',          Py_section.csv),
    #path('library/py/lezione/math',         Py_section.math),
    #path('library/py/lezione/json',         Py_section.json),
    #path('library/js/intro/',           Js_section.intro),
]
