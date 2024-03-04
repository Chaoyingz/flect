export type Json =
  | string
  | number
  | boolean
  | null
  | Json[]
  | {
      [k: string]: Json
    }
