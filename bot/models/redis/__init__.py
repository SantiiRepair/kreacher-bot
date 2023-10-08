from bot import r

# ------------------------------------------------------------------------
def add_to_queue(usuario_id, url, fecha):
    usuario_info = {'url': url, 'fecha': fecha}
    r.hset(cola, usuario_id, usuario_info)

def next_in_queue():
    proximo_usuario = r.hgetall(cola).popitem()
    
    usuario_id = proximo_usuario[0]
    usuario_info = proximo_usuario[1]
    
    print(f"Usuario ID: {usuario_id}")
    print(f"URL: {usuario_info[b'url'].decode()}")
    print(f"Fecha: {usuario_info[b'fecha'].decode()}")
    
    r.hdel(cola, usuario_id)
# ------------------------------------------------------------------------