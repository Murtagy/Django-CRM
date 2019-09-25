function add_url_param(param,value)
{
    var url = new URL(window.location.href);
    url.searchParams.set(param,value);
    window.location.href= url;
}