"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertCircle, CheckCircle2, Filter, Search } from "lucide-react"
import { useEffect, useState } from "react"

interface Alert {
    id: number
    severity: string
    title: string
    time: string
    status: string
    description?: string
}

export default function AlertsPage() {
    const [alerts, setAlerts] = useState<Alert[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        // Fetch alerts from API
        fetch("http://127.0.0.1:8000/api/alerts?limit=50")
            .then(res => res.json())
            .then(data => {
                // Transform API response to match component format
                const transformed = data.map((alert: any) => ({
                    id: alert.id,
                    severity: alert.severity,
                    title: alert.title,
                    time: alert.time,
                    status: alert.status,
                    description: alert.description
                }))
                setAlerts(transformed)
                setLoading(false)
            })
            .catch(err => {
                console.error("Failed to fetch alerts", err)
                setLoading(false)
            })
        
        // Refresh alerts every 5 seconds
        const interval = setInterval(() => {
            fetch("http://127.0.0.1:8000/api/alerts?limit=50")
                .then(res => res.json())
                .then(data => {
                    const transformed = data.map((alert: any) => ({
                        id: alert.id,
                        severity: alert.severity,
                        title: alert.title,
                        time: alert.time,
                        status: alert.status,
                        description: alert.description
                    }))
                    setAlerts(transformed)
                })
                .catch(err => console.error("Failed to refresh alerts", err))
        }, 5000)
        
        return () => clearInterval(interval)
    }, [])
    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h2 className="text-3xl font-bold tracking-tight">Alert Center</h2>
                <div className="flex gap-2">
                    <Button variant="outline" size="sm">
                        <Filter className="w-4 h-4 mr-2" /> Filter
                    </Button>
                    <Button size="sm">
                        Mark All Read
                    </Button>
                </div>
            </div>

            <div className="grid gap-4">
                <div className="flex bg-card p-2 rounded-lg border items-center px-4">
                    <Search className="w-4 h-4 text-muted-foreground mr-2" />
                    <input
                        className="bg-transparent border-none outline-none text-sm w-full placeholder:text-muted-foreground"
                        placeholder="Search alerts by ID, type, or region..."
                    />
                </div>

                <Card>
                    <CardHeader className="pb-3">
                        <CardTitle className="text-base text-muted-foreground uppercase tracking-wider text-xs">Recent Incidents</CardTitle>
                    </CardHeader>
                    <CardContent className="p-0">
                        {loading ? (
                            <div className="p-8 text-center text-muted-foreground">Loading alerts...</div>
                        ) : alerts.length === 0 ? (
                            <div className="p-8 text-center text-muted-foreground">No alerts found</div>
                        ) : (
                            <div className="divide-y divide-border/50">
                                {alerts.map(alert => (
                                <div key={alert.id} className="p-4 flex items-center justify-between hover:bg-muted/50 transition-colors cursor-pointer group">
                                    <div className="flex items-center gap-4">
                                        <div className={`w-2 h-2 rounded-full ${alert.severity === 'CRITICAL' ? 'bg-red-500 animate-pulse' : alert.severity === 'HIGH' ? 'bg-orange-500' : 'bg-blue-500'}`} />
                                        <div>
                                            <h4 className="font-semibold text-sm group-hover:text-primary transition-colors">{alert.title}</h4>
                                            <p className="text-xs text-muted-foreground flex items-center gap-2 mt-0.5">
                                                <span>ID: #{4920 + alert.id}</span>
                                                <span>•</span>
                                                <span>{alert.time}</span>
                                                <span>•</span>
                                                <span className={alert.status === 'Open' ? 'text-red-400' : 'text-green-400'}>{alert.status}</span>
                                            </p>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                        <Button size="sm" variant="outline" className="h-8">Details</Button>
                                        <Button size="sm" variant="ghost" className="h-8 w-8 p-0">
                                            <CheckCircle2 className="w-4 h-4 text-green-500" />
                                        </Button>
                                    </div>
                                </div>
                                ))}
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
