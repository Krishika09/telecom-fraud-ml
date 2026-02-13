"use client"

import { NetworkGraph } from "@/components/campaign/NetworkGraph"
import { ActiveCampaigns } from "@/components/dashboard/ActiveCampaigns"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Play, Pause, Share2 } from "lucide-react"

export default function CampaignPage() {
    return (
        <div className="space-y-4">
            <div className="flex items-center justify-between">
                <h2 className="text-3xl font-bold tracking-tight">Campaign Detection</h2>
                <div className="flex gap-2">
                    <Button variant="outline" size="sm">
                        <Pause className="w-4 h-4 mr-2" /> Pause Stream
                    </Button>
                    <Button size="sm">
                        <Share2 className="w-4 h-4 mr-2" /> Export Report
                    </Button>
                </div>
            </div>

            <div className="grid gap-4 md:grid-cols-3 h-[calc(100vh-140px)]">
                {/* Main Graph Area */}
                <Card className="col-span-2 flex flex-col">
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle>Live Behavioral Clustering</CardTitle>
                        <div className="text-xs text-muted-foreground font-mono">
                            Updated: Live
                        </div>
                    </CardHeader>
                    <CardContent className="flex-1 p-0 relative">
                        <NetworkGraph />

                        {/* Overlay Metrics */}
                        <div className="absolute top-4 right-4 bg-black/60 backdrop-blur p-2 rounded text-xs space-y-1 border border-white/10">
                            <div className="flex justify-between w-32">
                                <span className="text-zinc-400">Nodes:</span>
                                <span className="font-mono">3,492</span>
                            </div>
                            <div className="flex justify-between w-32">
                                <span className="text-zinc-400">Density:</span>
                                <span className="font-mono">0.84</span>
                            </div>
                            <div className="flex justify-between w-32">
                                <span className="text-zinc-400">Velocity:</span>
                                <span className="font-mono text-red-400">High</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* Sidebar List */}
                <div className="space-y-4 overflow-y-auto">
                    <Card>
                        <CardHeader>
                            <CardTitle>Identified Clusters</CardTitle>
                        </CardHeader>
                        <CardContent className="p-0">
                            <div className="p-4 pt-0">
                                {/* We can re-use ActiveCampaigns but stripping the card wrapper if we refactor,
                             or just render a similar list here manually for custom layout. 
                             I'll use a mocked list for variation. */}
                                {[1, 2, 3, 4, 5].map(i => (
                                    <div key={i} className="mb-3 p-3 bg-secondary/50 rounded-lg hover:bg-secondary cursor-pointer transition-colors border border-transparent hover:border-primary/30 group">
                                        <div className="flex justify-between items-start mb-2">
                                            <h4 className="font-semibold text-sm text-white group-hover:text-primary">Cluster #{490 + i}</h4>
                                            <span className="text-[10px] px-1.5 py-0.5 bg-red-500/20 text-red-500 rounded border border-red-500/30">CRITICAL</span>
                                        </div>
                                        <div className="text-xs text-zinc-400 space-y-1">
                                            <p>Type: Wangiri (One-Ring)</p>
                                            <p>Source Pattern: +92 300...</p>
                                            <p>Growth: +45 nodes/min</p>
                                        </div>
                                        <div className="mt-3 flex gap-2">
                                            <Button size="sm" variant="outline" className="h-6 text-[10px] w-full">Investigate</Button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    )
}
