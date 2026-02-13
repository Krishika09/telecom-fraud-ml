"use client"

import { ActiveCampaigns } from "@/components/dashboard/ActiveCampaigns"
import { CallIngestionChart } from "@/components/dashboard/CallIngestionChart"
import { RegionHeatmap } from "@/components/dashboard/RegionHeatmap"
import { ThreatIndex } from "@/components/dashboard/ThreatIndex"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Activity, ShieldAlert, PhoneOff, Users } from "lucide-react"

export default function DashboardPage() {
    return (
        <div className="space-y-4">
            <div className="flex items-center justify-between space-y-2">
                <h2 className="text-3xl font-bold tracking-tight">Intelligence Board</h2>
                <div className="flex items-center space-x-2">
                    <span className="relative flex h-3 w-3 mr-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
                    </span>
                    <span className="text-sm font-medium text-red-500">LIVE MONITORING</span>
                </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <ThreatIndex />

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Suspicious Signals</CardTitle>
                        <PhoneOff className="h-4 w-4 text-orange-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">1,240</div>
                        <p className="text-xs text-muted-foreground">+180 since 00:00</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Est. Victims Saved</CardTitle>
                        <Users className="h-4 w-4 text-green-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">45,231</div>
                        <p className="text-xs text-muted-foreground">+12% from yesterday</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Network Load</CardTitle>
                        <Activity className="h-4 w-4 text-blue-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">92%</div>
                        <p className="text-xs text-muted-foreground">Optimal capacity</p>
                    </CardContent>
                </Card>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <div className="col-span-4">
                    <CallIngestionChart />
                </div>
                <div className="col-span-3">
                    <ActiveCampaigns />
                </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-2">
                <RegionHeatmap />
                {/* Placeholder for Anomaly Log or something else */}
                <Card className="col-span-1">
                    <CardHeader>
                        <CardTitle>Emerging Anomalies</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            <div className="flex items-start space-x-4 p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
                                <ShieldAlert className="w-5 h-5 text-yellow-500 mt-0.5" />
                                <div>
                                    <h4 className="font-semibold text-yellow-500 text-sm">Protocol Deviation: SIP-Trunk #49</h4>
                                    <p className="text-xs text-zinc-400 mt-1">Unusual signaling volume detected from +92 gateway. Investigating auto-block rules.</p>
                                    <p className="text-[10px] text-zinc-500 mt-2">Detected 45s ago</p>
                                </div>
                            </div>
                            <div className="flex items-start space-x-4 p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                                <Activity className="w-5 h-5 text-blue-500 mt-0.5" />
                                <div>
                                    <h4 className="font-semibold text-blue-500 text-sm">Model Drift Warning</h4>
                                    <p className="text-xs text-zinc-400 mt-1">Confidence score distribution shifting left. Retraining recommended.</p>
                                    <p className="text-[10px] text-zinc-500 mt-2">Detected 2m ago</p>
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
