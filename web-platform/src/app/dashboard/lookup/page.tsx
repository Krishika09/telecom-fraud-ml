"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Search, ShieldCheck, ShieldAlert, AlertTriangle, Loader2 } from "lucide-react"
import { useState } from "react"

export default function LookupPage() {
    const [number, setNumber] = useState("")
    const [result, setResult] = useState<any>(null)
    const [loading, setLoading] = useState(false)

    const handleLookup = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!number) return

        setLoading(true)
        setResult(null)

        try {
            const res = await fetch("http://127.0.0.1:8000/api/check-number", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ number })
            })
            const data = await res.json()
            // Simulate delay for dramatic effect
            setTimeout(() => {
                setResult(data)
                setLoading(false)
            }, 800)
        } catch (err) {
            console.error(err)
            setLoading(false)
        }
    }

    return (
        <div className="max-w-2xl mx-auto space-y-8 pt-10">
            <div className="text-center space-y-2">
                <h2 className="text-3xl font-bold tracking-tight">Citizen Risk Lookup</h2>
                <p className="text-muted-foreground">Verify any number against the National Fraud Intelligence Grid.</p>
            </div>

            <Card className="border-primary/20 bg-card/50 backdrop-blur">
                <CardContent className="p-6">
                    <form onSubmit={handleLookup} className="flex gap-4">
                        <div className="relative flex-1">
                            <Search className="absolute left-3 top-3 h-5 w-5 text-muted-foreground" />
                            <input
                                value={number}
                                onChange={(e) => setNumber(e.target.value)}
                                placeholder="Enter phone number (e.g., +91 99999...)"
                                className="w-full flex h-11 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 pl-10"
                            />
                        </div>
                        <Button type="submit" size="lg" disabled={loading} className="w-32">
                            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Scan"}
                        </Button>
                    </form>
                </CardContent>
            </Card>

            {result && (
                <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                    <Card className={`border-l-4 ${result.status === 'SAFE' ? 'border-l-green-500 border-green-500/20' : result.status === 'SUSPICIOUS' ? 'border-l-yellow-500 border-yellow-500/20' : 'border-l-red-500 border-red-500/20'}`}>
                        <CardHeader>
                            <div className="flex items-center justify-between">
                                <CardTitle className="text-lg">Scan Result for {number}</CardTitle>
                                <div className={`px-3 py-1 rounded-full text-xs font-bold ${result.status === 'SAFE' ? 'bg-green-500/20 text-green-400' : result.status === 'SUSPICIOUS' ? 'bg-yellow-500/20 text-yellow-400' : 'bg-red-500/20 text-red-500 animate-pulse'}`}>
                                    {result.status}
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div className="p-4 bg-background/50 rounded-lg border space-y-1">
                                    <span className="text-xs text-muted-foreground uppercase">Risk Score</span>
                                    <div className="text-3xl font-mono font-bold">{result.risk_score}/100</div>
                                </div>
                                <div className="p-4 bg-background/50 rounded-lg border space-y-1">
                                    <span className="text-xs text-muted-foreground uppercase">Category</span>
                                    <div className="text-lg font-semibold">{result.category}</div>
                                </div>
                                <div className="p-4 bg-background/50 rounded-lg border space-y-1">
                                    <span className="text-xs text-muted-foreground uppercase">User Reports</span>
                                    <div className="text-lg font-semibold">{result.reports || 0}</div>
                                </div>
                                <div className="p-4 bg-background/50 rounded-lg border space-y-1">
                                    <span className="text-xs text-muted-foreground uppercase">Last Active</span>
                                    <div className="text-lg font-semibold">{result.last_active || "Unknown"}</div>
                                </div>
                                {result.cluster_id && (
                                    <div className="p-4 bg-background/50 rounded-lg border space-y-1">
                                        <span className="text-xs text-muted-foreground uppercase">Cluster ID</span>
                                        <div className="text-lg font-semibold font-mono">{result.cluster_id}</div>
                                    </div>
                                )}
                                {result.fraud_type && result.fraud_type !== "Legitimate" && (
                                    <div className="p-4 bg-background/50 rounded-lg border space-y-1">
                                        <span className="text-xs text-muted-foreground uppercase">Fraud Type</span>
                                        <div className="text-lg font-semibold">{result.fraud_type}</div>
                                    </div>
                                )}
                            </div>
                            
                            {result.explanation && (
                                <div className="p-4 bg-secondary/30 rounded-lg text-sm text-muted-foreground">
                                    <p className="font-semibold mb-2">Explanation:</p>
                                    <p>{result.explanation}</p>
                                </div>
                            )}

                            <div className="flex items-start gap-3 p-4 bg-secondary/30 rounded-lg text-sm text-muted-foreground">
                                {result.status === 'SAFE' ? <ShieldCheck className="w-5 h-5 text-green-500 flex-shrink-0" /> : result.status === 'SUSPICIOUS' ? <AlertTriangle className="w-5 h-5 text-yellow-500 flex-shrink-0" /> : <ShieldAlert className="w-5 h-5 text-red-500 flex-shrink-0" />}
                                <p>
                                    {result.explanation || (result.status === 'SAFE'
                                        ? "This number has shown consistent legitimate behavior patterns over the last 90 days."
                                        : result.status === 'SUSPICIOUS'
                                            ? "This number exhibits irregular calling patterns. Exercise caution."
                                            : "CRITICAL WARNING: This number is part of a verified fraud campaign. Do not answer.")}
                                </p>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            )}
        </div>
    )
}
