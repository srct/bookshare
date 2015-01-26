from django.shortcuts import render

# stuff copied out of the website views

# saved searches
    # need to implement haystack stuff first

### VIEWS ###

@login_required
def create_lookout(request, username):

    lookout_form = LookoutForm()

    if request.method == 'POST':
        lookout_form = LookoutForm( request.POST )
        if lookout_form.is_valid():
            lookout = lookout_form.save(commit=False)
            lookout.ISBN = lookout.ISBN.strip()
            lookout.owner = request.user.seller
            lookout.save()
            return redirect( 'profile', username )

    return render(request, 'create_lookout.html', {
        'lookout_form': lookout_form,
    },
    )


