// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

const cspHeader =
  "default-src 'self'; " +
  "script-src 'self' 'unsafe-inline' 'unsafe-eval' http: https: data: blob:; " +
  "style-src 'self' 'unsafe-inline' https:; " +
  "img-src 'self' data: https: http: blob:; " +
  "font-src 'self' data: https:; " +
  "connect-src 'self' http://localhost:5000 ws: wss:; " +
  "frame-src 'self' https:; " +
  "object-src 'none'";

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:5000'
    }
  },
  vite: {
    base: '/',
    server: {
      host: '0.0.0.0',
      fs: {
        allow: ['**']
      },
      proxy: {
        '/uploads': {
          target: 'http://localhost:5000',
          changeOrigin: true,
          secure: false,
        }
      }
    },
    plugins: [
      tailwindcss(),
      {
        name: 'csp-headers',
        configureServer(server) {
          server.middlewares.use(function(_req, res, next) {
            res.setHeader('Content-Security-Policy', cspHeader);
            next();
          });
        }
      }
    ]
  },
  nitro: {
    proxy: {
      '/uploads': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        pathRewrite: { '^/uploads': '/uploads' },
      }
    },
    headers: {
      'Content-Security-Policy': cspHeader
    }
  },
  app: {
    head: {
      title: 'FLAVORIA Restaurant',
      meta: [
        {
          name: 'viewport',
          content: 'width=device-width, initial-scale=1'
        },
        {
          name: 'content-security-policy',
          content: cspHeader
        }
      ]
    }
  }
})
