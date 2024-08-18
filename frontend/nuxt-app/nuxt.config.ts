// https://nuxt.com/docs/api/configuration/nuxt-config

import {definePreset} from "@primevue/themes";
import Aura from "@primevue/themes/aura"

const customTheme = definePreset(Aura, {
  semantic: {
    primary: {
      50: '{indigo.50}',
      100: '{indigo.100}',
      200: '{indigo.200}',
      300: '{indigo.300}',
      400: '{indigo.400}',
      500: '{indigo.500}',
      600: '{indigo.600}',
      700: '{indigo.700}',
      800: '{indigo.800}',
      900: '{indigo.900}',
      950: '{indigo.950}'
    }
  }
});


export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  modules: ['@primevue/nuxt-module', "@pinia/nuxt", "@nuxtjs/mdc", "@nuxt/image"],
  primevue:{
    options:{
      theme:{
        preset:customTheme,
        options:{
          prefix:'p'
        }
      },
    }
  },
  pinia: {
    storesDirs: ['./stores/**'],
  },
  alias: {
    pinia: "/node_modules/@pinia/nuxt/node_modules/pinia/dist/pinia.mjs"
  },
  vite: {
    server: {
      hmr: {
        protocol: "http",
        host: 'localhost',
        clientPort: 3000,
        port: 3000,
      },
    },
  },
  markdownit: {
    runtime: true
  }
})