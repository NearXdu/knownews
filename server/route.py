from views import * 


def setup_routes(app):
    app.router.add_get('/', news_list_handle)
    app.router.add_get('/detail/{news_id}', news_detail_handle)
    app.router.add_get('/keyword/{keyword}', keywords_explain_handle)
    #app.router.add_get('/{name}', handle)
