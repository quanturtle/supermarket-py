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
                        <div className="w-full mx-auto max-w-screen-2xl">
                            <CustomNavbar />
                        </div>
                        <div className="container mx-auto flex-1 px-4 py-6 md:px-6 lg:px-8 max-w-7xl">
                            {children}
                        </div>
                        <div className="w-full mx-auto max-w-screen-2xl">
                            <CustomFooter />
                        </div>
                    </div>
                </CartProvider>
            </body>
        </html>
    )
}