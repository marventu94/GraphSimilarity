// Seleccionar la base de datos "graph_similarity"
db = db.getSiblingDB("graph_similarity");

// Crear la colección "users" si no existe y agregar los usuarios
db.users.insertMany([
  {
    username: "freemium_user",
    password: "482c811da5d5b4bc6d497ffa98491e38", // Hash md5 ==> password password123
    subscription_type: "FREEMIUM"
  },
  {
    username: "premium_user",
    password: "96b33694c4bb7dbd07391e0be54745fb", // Hash md5 ==> password password456
    subscription_type: "PREMIUM"
  }
]);

print("Database 'graph_similarity' and collection 'users' created with initial data.");
