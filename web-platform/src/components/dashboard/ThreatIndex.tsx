"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useSocket } from "@/context/SocketContext"
import { AlertTriangle } from "lucide-react"

export function ThreatIndex() {
    // Mock logic: derive index from recent calls for now or random
    // ideally backend sends "threat_level"
    // For demo, we'll randomize it slightly based on socket data

    const { isConnected } = useSocket()

    // In a real app, this would be computed from the stream
    const threatLevel = isConnected ? 7.8 : 0

    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                    National Threat Index
                </CardTitle>
                <AlertTriangle className="h-4 w-4 text-destructive" />
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold">{threatLevel}/10</div>
                <p className="text-xs text-muted-foreground">
                    +2.1% from last hour
                </p>
                <div className="mt-4 h-2 w-full bg-secondary rounded-full overflow-hidden">
                    <div
                        className="h-full bg-destructive transition-all duration-500"
                        style={{ width: `${threatLevel * 10}%` }}
                    />
                </div>
            </CardContent>
        </Card>
    )
}
