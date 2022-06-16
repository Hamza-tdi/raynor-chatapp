def generate_partial_key(client_pk, server_pvk, server_pk):
    partial_key = server_pk ** server_pvk
    partial_key = partial_key % client_pk
    return partial_key