const { Telegraf, Markup } = require('telegraf');
require('dotenv').config();

// Configuration du bot
const bot = new Telegraf(process.env.BOT_TOKEN);

// Handler /start - Message d'accueil avec photo et boutons
bot.start(async (ctx) => {
  try {
    // Essayer d'envoyer la photo d'abord
    try {
      await ctx.replyWithPhoto(
        { source: 'logo.jpg' }, // Utilise le logo.jpg à la racine du projet
        {
          caption: `✨ BIENVENUE CHEZ PUFF LENS/BETHUNE ✨
� Puffs Premium & Tabacs de Qualité Supérieure �

🔥 Commandes rapides - Livraison express �`,
          reply_markup: {
            inline_keyboard: [
              [
                {
                  text: "📱 Ouvrir la mini-app",
                  web_app: { url: process.env.MINI_APP_URL }
                }
              ],
              [
                {
                  text: "📢 Canal ↗",
                  url: process.env.CANAL_URL
                },
                {
                  text: "📞 Contacter ↗", 
                  url: process.env.CONTACT_URL
                },
                {
                  text: "📷 Instagram ↗", 
                  url: process.env.INSTAGRAM_URL
                }
              ]
            ]
          }
        }
      );
    } catch (photoError) {
      // Si la photo ne fonctionne pas, envoyer juste le texte avec les boutons
      console.log('Photo non trouvée, envoi du texte seulement:', photoError.message);
      await ctx.reply(`✨ **BIENVENUE CHEZ PUFF LENS/BETHUNE** ✨

� Puffs Premium & Tabacs de Qualité Supérieure �

🔥 Commandes rapides - Livraison express �`, {
        reply_markup: {
          inline_keyboard: [
            [
              {
                text: "📱 Ouvrir la mini-app",
                web_app: { url: process.env.MINI_APP_URL }
              }
            ],
            [
              {
                text: "📢 Canal ↗",
                url: process.env.CANAL_URL
              },
              {
                text: "📞 Contacter ↗", 
                url: process.env.CONTACT_URL
              }
            ]
          ]
        },
        parse_mode: 'Markdown'
      });
    }
  } catch (error) {
    console.error('Erreur dans /start:', error);
    await ctx.reply('Désolé, une erreur est survenue. Réessayez plus tard.');
  }
});

// Handler /help - Commande d'aide
bot.help((ctx) => {
  ctx.reply(`🤖 *Commandes disponibles:*
/start - Lancer le bot et voir la mini-app
/help - Voir cette aide

📱 *Mini App:* Puffs Premium & Tabacs de Qualité
📢 *Canal:* Les dernières nouveautés exclusives
📞 *Contact:* Commande rapide sur Snapchat
📷 *Instagram:* Photos et promotions`, {
    parse_mode: 'Markdown'
  });
});

// Handler pour les messages non reconnus
bot.on('message', (ctx) => {
  ctx.reply('Utilisez /start pour accéder à la mini-app Puff Lens/Bethune 💨');
});

// Gestion des erreurs
bot.catch((err, ctx) => {
  console.error(`Erreur pour ${ctx.updateType}:`, err);
  ctx.reply('Une erreur est survenue. Réessayez plus tard.');
});

// Démarrage du bot avec délai pour éviter les conflits
setTimeout(() => {
  bot.launch()
    .then(() => {
      console.log('🤖 Puff Lens/Bethune Bot démarré avec succès!');
    })
    .catch((err) => {
      console.error('❌ Erreur au démarrage du bot:', err);
    });
}, 3000); // Attendre 3 secondes

// Arrêt propre du bot
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));

module.exports = bot;
