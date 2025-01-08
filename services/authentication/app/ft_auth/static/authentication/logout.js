function logout(event)
{
    loadPageEvent(event,'/logout/');
    setTimeout(() =>
    {
        loadPage('/login/')
    }, 2000)
}