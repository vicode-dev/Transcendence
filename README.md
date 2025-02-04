# 🏓 Transcendence - 42Cursus Project

Welcome to **Transcendence**, the final project of the 42Cursus common core program. 

## ✨ Project Overview

**Transcendence** is about making a website that allows users to play pong.


### 🎯 Key Objectives:

### 📚 Features

#### Web
- [x] [Use a Framework to build the backend](#framework-for-backend)
- [x] [Use a framework or a toolkit to build the frontend](#framework-for-front-end)
- [x] [Use a database for the backend](#database-for-backend)
- [x] [Store the score of a tournament in the Blockchain](#blockchain)

#### User Management
- [x]  [Standard user management, authentication, user across tournaments](#standard-user-management)
- [x]  [Implementing a remote authentication](#remote-authentication)

#### Gameplay and user experience
- [x]  [Remote players](#remote-players)
- [x]  [Multiplayers (more than 2 in the same game)](#multiple-players)
- [x]  [Add Another Game with User History and Matchmaking](#another-game)
- [ ]  Game Customization Options
- [ ]  Live chat

#### AI-Algo
- [x]  [Introduce an AI Opponent](#ai-opponent)
- [ ]  User and Game Stats Dashboards

#### Cybersecurity
- [ ]  Implement WAF/ModSecurity with Hardened Configuration and HashiCorp Vault for Secrets Management
- [x]  [GDPR Compliance Options with User Anonymization, Local Data Management, and Account Deletion](#gdpr)
- [x]  [Implement Two-Factor Authentication (2FA) and JWT](#2fa)

#### Devops
- [x]  [Infrastructure Setup for Log Management](#elk)
- [x]  [Monitoring system](#monitoring-system)
- [x]  [Designing the Backend as Microservices](#backend-as-microservices)

#### Graphics
- [x]  [Use of advanced 3D techniques](#3d-techniques)

#### Accessibility
- [x]  [Support on all devices](#support-on-all-devices)
- [x]  [Expanding Browser Compatibility](#browser-compatibility)
- [x]  [Multiple language supports](#multiple-languages)
- [ ]  Add accessibility for Visually Impaired Users
- [x]  [Server-Side Rendering (SSR) Integration](#ssr-integration)

#### Server-Side Pong
- [x]  [Replacing Basic Pong with Server-Side Pong and Implementing an API](#server-side-pong)
- [x]  [Enabling Pong Gameplay via CLI against Web Users with API Integration](#cli)

### Detailed Features

#### Web

##### <i>Framework for backend</i>
We used Django for our backend development.

##### <i>Framework for front-end</i>
We used Bootstrap toolkit in addition of the vanilla Javascript for our frontend

##### <i>Database for backend</i>
We used a database for our backend. The database itself is PostgresSQL.

##### <i>Blockchain</i>
We store the tournament scores on a blockchain. The blockchain is Ethereum and the language used for smart contract development is Solidity. 

#### User Management

##### <i>Standard user management</i>
Users can subscribe to the website and registered users can log in in a secure way. Users can select a unique display name to play the tournaments. They can update their information, upload an avatar (there is a default avatar if they don't provide one), add others as friends and view their online status. User profiles display stats (their wins and losses) and each user has a match history. 

##### <i>Remote authentication</i>
Implementation of the following system: OAuth 2.0 authentication with 42.

#### Gameplay and user experience 

##### <i>Remote players</i>
It is possible for two players, using two different computers, to access the website and play pong together. Network issues have been taken into account.

##### <i>Multiple players</i>
Pong can be played by 2 or 4 players.

##### <i>Another game</i>
It is possible to play another game than pong : connect 4. There is an history and players can join a game by using the matchmaking system. 

#### AI-Algo

##### <i>AI opponent</i>
It is possible to play against an AI in the CLI (Command-Line Interface).

#### Cybersecurity

##### <i>GDPR</i>
We are compliant with the GDPR. Users are able to request anonymization of their personal data, which ensure that their identity and sensitive information are protected. They can also view, edit or delete their personal information stored within the system. They can request the permanent deletion fo their account.

##### <i>2FA</i>
We implemented Two-Factor Authentication (2FA) and we utilize JSON Web Tokens (JWT) as a secure method for authentication and authorization.

#### Devops

##### <i>ELK</i>
We established a robust infrastructure for log management and analysis using the ELK stack (Elasticsearch, Logstash, Kibana).

##### <i>Monitoring system</i>
We set up a monitoring system using Prometheus and Grafana.

##### <i>Backend as microservices</i>
The backend follows microservices best practices.

#### Graphics

##### <i>3D techniques</i>
Players can choose to play pong in 3D. We used ThreeJS/WebGL to create the graphics.

#### Accessibility

##### <i>Support on all devices</i>
The website is designed in mobile first, responsive, supported on all devices.

##### <i>Browser compatibility</i>
The website is compatible with at least Chrome, Chrome-based and Firefox.

##### <i>Multiple languages</i>
Players can change the language of the website. The supported languages are English, French, Spanish and Dutch.

##### <i>SSR integration</i>
We integrated Server-Side Rendering (SSR) to enhance the performance and SIO (Search Engine Optimization) of the website.

#### Server-Side Pong

##### <i>Server-side pong</i>
We replaced the basic pong game with a server-side pong game, accompanied by the implementation of an API.

##### <i>CLI</i>
We developed a Command-Line Interface (CLI) that allows users to play pong against players using the web version of the game.  

### Out of scope

We added a system of tournament that allows distant players to play together.
Users can pick a theme. 


## 🛠️ Installation & Compilation Guide

### 📦 Dependencies

1. Make sure you have the following installed:

- **Docker**
- **Docker compose**

2. Set up the environment variables by creating a .env file in the root directory. The required variables are:

```
POSTGRES_PASSWORD=your_postgres_password
ELASTIC_PASSWORD=your_elastic_password
DISCORD_WEBHOOK_URL=your_discord_webhook_url
KIBANA_ENCRYPTION_KEY=your_kibana_encryption_key
DOMAIN_NAME=your_domain_name
JWT_SECRET_KEY=your_jwt_secret_key
SALT=your_salt
KIBANA_PASSWD=your_kibana_password
DJANGO_SECRET=your_django_secret
CLIENT_42_ID=your_client_42_id
CLIENT_42_SECRET=your_client_42_secret
```

### 🏗️ Compilation

Once you have all the dependencies, you can compile **Transcendence** using the following `Makefile` commands:

```bash
make
```

## 🚀 Usage


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
