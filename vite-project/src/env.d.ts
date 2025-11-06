/// <reference types="vite/client" />

// Allow importing CSS files in TS
declare module '*.css'

// Allow importing SVG and other assets as modules returning a string URL
declare module '*.svg' {
  const src: string
  export default src
}

declare module '*.png'
declare module '*.jpg'
declare module '*.jpeg'
declare module '*.gif'
