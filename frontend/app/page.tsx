import { CustomHero } from "@/components/custom-hero"
import { CustomFooter } from "@/components/custom-footer"
import { CustomNavbar } from "@/components/custom-navbar"

export default function Home() {
  return (
    <main className="flex min-h-screen container mx-auto flex-col bg-gray-50">
      <div className="flex-1 flex items-center justify-center">
        <CustomHero />
      </div>
    </main>
  )
}