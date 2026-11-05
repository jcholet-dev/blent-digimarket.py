# Blent DigiMarket API

## 📋 Description du Projet
`blent-digimarket-api` est une API RESTful conçue en Python/Flask servant de backend pour une plateforme de commerce numérique ("DigiMarket"). Elle permet la gestion sécurisée des utilisateurs, la gestion d'un catalogue de produits, le traitement des commandes et le suivi des cagnottes / transactions.

L'application s'appuie sur une architecture basée sur les rôles (**RBAC - Role-Based Access Control**) séparant strictement les privilèges des utilisateurs.

---

## 👥 Profils Utilisateurs & Permissions

L'application distingue deux types de profils :

* **Clients :**
  * Création de compte et authentification.
  * Consultation du catalogue produits.
  * Passation et suivi de l'état des commandes.
  * Gestion du solde et de la cagnotte personnelle.

* **Administrateurs :**
  * Gestion globale du catalogue produits (ajout, modification, suppression).
  * Suivi, modération et modification du statut de l'ensemble des commandes.
  * Administration des comptes utilisateurs.

---

## 🚀 Étape 1 : Authentification & Gestion des Utilisateurs

Cette première étape couvre la mise en place de la brique de sécurité fondamentale : la création des comptes et la délivrance des jetons de connexion **JWT (JSON Web Token)**.

### 📜 Règles Métier
1. **Unicité :** Chaque compte doit être rattaché à une adresse email unique.
2. **Sécurité des mots de passe :** Les mots de passe sont hachés avant stockage en base de données.
3. **Authentification :** Une connexion réussie délivre un jeton JWT contenant l'identifiant et le rôle de l'utilisateur, nécessaire pour sécuriser les routes ultérieures.

---

## 🛠️ Spécifications des Endpoints (Étape 1)

### 1. Inscription d'un utilisateur
Permet à un nouvel utilisateur (client par défaut) de créer un compte.

* **URL :** `/api/auth/register`
* **Méthode :** `POST`
* **Headers :** `Content-Type: application/json`
* **Corps de la requête (JSON) :**
  ```json
  {
    "email": "user@example.com",
    "password": "MotDePasseSecurise123!",
    "first_name": "Jean",
    "last_name": "Dupont"
  }
  ```
* **Réponse de succès (`201 Created`) :**
  ```json
  {
    "message": "Utilisateur créé avec succès",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "Jean",
      "last_name": "Dupont",
      "role": "client"
    }
  }
  ```
* **Erreurs possibles :**
  * `400 Bad Request` : Champs requis manquants ou format invalide.
  * `409 Conflict` : Adresse email déjà utilisée.

---

### 2. Connexion et génération de Token JWT
Permet à un utilisateur enregistré de s'authentifier et de récupérer son jeton d'accès.

* **URL :** `/api/auth/login`
* **Méthode :** `POST`
* **Headers :** `Content-Type: application/json`
* **Corps de la requête (JSON) :**
  ```json
  {
    "email": "user@example.com",
    "password": "MotDePasseSecurise123!"
  }
  ```
* **Réponse de succès (`200 OK`) :**
  ```json
  {
    "message": "Connexion réussie",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "role": "client"
    }
  }
  ```
* **Erreurs possibles :**
  * `401 Unauthorized` : Identifiants ou mot de passe incorrects.

---

## 🔒 Utilisation du Token JWT
Pour accéder aux routes protégées qui seront développées dans les étapes suivantes, le jeton JWT doit être envoyé dans l'entête HTTP de chaque requête :

```http
Authorization: Bearer <votre_access_token>
```
