import type React from "react"
import "@/app/globals.css"
import { CartProvider } from "@/hooks/use-cart"
import { CustomNavbar } from "@/components/custom-navbar"
import { CustomFooter } from "@/components/custom-footer"

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <CartProvider>
          <div className="flex min-h-screen flex-col bg-gray-50">
            <CustomNavbar />
            <div className="container mx-auto flex-1 px-4 py-6 md:px-6 max-w-7xl">{children}</div>
            <CustomFooter />
          </div>
        </CartProvider>
      </body>
    </html>
  )
}


import './globals.css'

export const metadata = {
      generator: 'v0.dev'
    };
