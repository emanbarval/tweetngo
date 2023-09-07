# tweetngo
Clon de Twitter realizado con Django y graphql

Utilizando Django y PostgreSQL se crea un API GraphQL que da servicio a una app y resuelve las siguientes historias de usuario:

- Un usuario puede registrarse introduciendo su email y eligiendo un nombre de usuario libre y una contraseña
- Un usuario debe ser capaz de logarse utilizando email y contraseña.
- Un usuario debe poder cambiar su contraseña.
- Un usuario debe poder restaurar su contraseña recibiendo un email con un magic link.
- Un usuario puede publicar una idea como un texto corto en cualquier momento.
- Un usuario puede establecer la visibilidad de una idea: publica (todos pueden verla), protegida (solo otros usuarios que siguen al usuario de la idea pueden verla) y privada (solo el usuario que creó la idea puede verla)
- Un usuario puede establecer la visibilidad de una idea en el momento de su creación o editarla posteriormente.
- Un usuario puede consultar todas las ideas que ha publicado ordenadas de mas recientes a mas antiguas.
- Un usuario puede borrar una idea publicada.
- Un usuario puede solicitar seguir a otro usuario
- Un usuario puede ver el listado de solicitudes de seguimiento recibidas y aprobarlas o denegarlas
- Un usuario puede ver el listado de gente a la que sigue
- Un usuario puede ver el listado de gente que le sigue
- Un usuario puede dejar de seguir a alguien
- Un usuario puede eliminar a otro usuario de su lista de seguidores
- Un usuario puede realizar una búsqueda de otros usuarios introduciendo un nombre de usuario o parte de uno
- Un usuario puede ver la lista de ideas de cualquier otro usuario, teniendo en cuenta la visibilidad de cada idea.
- Un usuario puede ver un timeline de ideas compuesto por sus propias ideas y las ideas de los usuarios a los que sigue, teniendo en cuenta la visibilidad de cada idea.
- Un usuario debe recibir una notificación cada vez que un usuario al que sigue publica una idea nueva a la que tiene acceso.
