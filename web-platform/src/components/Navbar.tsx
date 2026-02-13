import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ShieldAlert } from "lucide-react"

export function Navbar() {
    return (
        <nav className="fixed w-full z-50 top-0 start-0 border-b border-white/10 bg-background/80 backdrop-blur-md">
            <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
                <Link href="/" className="flex items-center space-x-3 rtl:space-x-reverse">
                    <ShieldAlert className="h-8 w-8 text-primary" />
                    <span className="self-center text-2xl font-bold whitespace-nowrap text-white">SATARK</span>
                </Link>
                <div className="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
                    <Link href="/dashboard">
                        <Button variant="default" className="font-bold">
                            Access Intelligence Grid
                        </Button>
                    </Link>
                </div>
                <div className="items-center justify-between hidden w-full md:flex md:w-auto md:order-1" id="navbar-sticky">
                    <ul className="flex flex-col p-4 md:p-0 mt-4 font-medium border border-gray-100 rounded-lg md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0">
                        <li>
                            <Link href="#" className="block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-primary md:p-0" aria-current="page">Vision</Link>
                        </li>
                        <li>
                            <Link href="#" className="block py-2 px-3 text-gray-300 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-primary md:p-0">Technology</Link>
                        </li>
                        <li>
                            <Link href="#" className="block py-2 px-3 text-gray-300 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-primary md:p-0">Privacy</Link>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    )
}
