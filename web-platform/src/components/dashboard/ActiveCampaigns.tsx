"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge" // We need to create badge or use div
import { useEffect, useState } from "react"

// Simple mock Badge since we don't have it yet
function SimpleBadge({ children, variant }: { children: React.ReactNode, variant: "default" | "destructive" }) {
    const color = variant === "destructive" ? "bg-red-500/20 text-red-400 border-red-500/50" : "bg-primary/20 text-primary border-primary/50"
    return (
        <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 ${color}`}>
            {children}
        </span>
    )
}

interface Campaign {
    id: string
    name: string
    risk_score: number
    affected_users: number
    status: string
}

export function ActiveCampaigns() {
    const [campaigns, setCampaigns] = useState<Campaign[]>([])

    useEffect(() => {
        // Fetch initial campaigns
        fetch("http://127.0.0.1:8000/api/campaigns")
            .then(res => res.json())
            .then(data => setCampaigns(data))
            .catch(err => console.error("Failed to fetch campaigns", err))

        // In real app, we would listen to socket updates for campaigns too
    }, [])

    return (
        <Card className="col-span-3">
            <CardHeader>
                <CardTitle>Active Intelligence Clusters</CardTitle>
            </CardHeader>
            <CardContent>
                <div className="space-y-4">
                    {campaigns.length === 0 ? (
                        <p className="text-muted-foreground">Scanning network...</p>
                    ) : (
                        campaigns.map(campaign => (
                            <div key={campaign.id} className="flex items-center justify-between p-3 border rounded-lg bg-black/20">
                                <div>
                                    <div className="flex items-center gap-2">
                                        <p className="font-medium text-sm">{campaign.name}</p>
                                        <SimpleBadge variant="destructive">Risk: {campaign.risk_score}</SimpleBadge>
                                    </div>
                                    <p className="text-xs text-muted-foreground mt-1">
                                        Affecting {campaign.affected_users.toLocaleString()} users • Status: {campaign.status}
                                    </p>
                                </div>
                                <div className="text-right">
                                    <span className="text-xs font-mono text-primary cursor-pointer hover:underline">
                                        View Analysis &rarr;
                                    </span>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </CardContent>
        </Card>
    )
}
