"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import {
    LayoutDashboard,
    ShieldAlert,
    Network,
    Activity,
    UserSearch,
    Settings,
    Menu
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { useState } from "react"

const routes = [
    {
        label: "Intelligence Board",
        icon: LayoutDashboard,
        href: "/dashboard",
        color: "text-sky-500",
    },
    {
        label: "Campaign Detection",
        icon: Network,
        href: "/dashboard/campaigns",
        color: "text-violet-500",
    },
    {
        label: "Alert Center",
        icon: ShieldAlert,
        href: "/dashboard/alerts",
        color: "text-red-500",
    },
    {
        label: "Live Threat Stream",
        icon: Activity,
        href: "/dashboard/stream",
        color: "text-green-500",
    },
    {
        label: "Citizen Risk Lookup",
        icon: UserSearch,
        href: "/dashboard/lookup",
        color: "text-pink-700",
    },
    {
        label: "Admin Controls",
        icon: Settings,
        href: "/dashboard/admin",
    },
]

export function Sidebar() {
    const pathname = usePathname()
    const [isMobileOpen, setIsMobileOpen] = useState(false)

    return (
        <>
            {/* Mobile Trigger */}
            <div className="md:hidden p-4 flex items-center justify-between bg-background border-b z-50 sticky top-0">
                <h1 className="font-bold text-xl text-primary">SATARK</h1>
                <Button variant="ghost" size="icon" onClick={() => setIsMobileOpen(!isMobileOpen)}>
                    <Menu />
                </Button>
            </div>

            <div className={cn(
                "space-y-4 py-4 flex flex-col h-full bg-card text-card-foreground border-r transition-transform md:translate-x-0 fixed md:relative z-40 w-72",
                isMobileOpen ? "translate-x-0" : "-translate-x-full"
            )}>
                <div className="px-3 py-2 flex-1">
                    <Link href="/dashboard" className="flex items-center pl-3 mb-14">
                        <div className="relative w-8 h-8 mr-4">
                            {/* Logo placeholder */}
                            <div className="w-full h-full bg-primary rounded-full animate-pulse" />
                        </div>
                        <h1 className="text-2xl font-bold font-mono tracking-widest text-primary">
                            SATARK
                        </h1>
                    </Link>
                    <div className="space-y-1">
                        {routes.map((route) => (
                            <Link
                                key={route.href}
                                href={route.href}
                                className={cn(
                                    "text-sm group flex p-3 w-full justify-start font-medium cursor-pointer hover:text-primary hover:bg-primary/10 rounded-lg transition",
                                    pathname === route.href ? "text-primary bg-primary/10" : "text-zinc-400"
                                )}
                            >
                                <div className="flex items-center flex-1">
                                    <route.icon className={cn("h-5 w-5 mr-3", route.color)} />
                                    {route.label}
                                </div>
                            </Link>
                        ))}
                    </div>
                </div>
                <div className="px-3 py-2">
                    <div className="text-xs text-zinc-500 text-center">
                        SATARK Intelligence Grid v1.0
                    </div>
                </div>
            </div>

            {/* Mobile Overlay */}
            {isMobileOpen && (
                <div
                    className="fixed inset-0 bg-black/50 z-30 md:hidden"
                    onClick={() => setIsMobileOpen(false)}
                />
            )}
        </>
    )
}
