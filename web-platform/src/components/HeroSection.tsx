"use client"

import { Button } from "@/components/ui/button"
import { motion } from "framer-motion"
import { ShieldCheck, EyeOff, Activity } from "lucide-react"

export function HeroSection() {
    return (
        <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 overflow-hidden">
            <div className="container px-4 mx-auto text-center relative z-10">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <span className="inline-block py-1 px-3 rounded-full bg-primary/10 text-primary text-sm font-semibold mb-6 border border-primary/20">
                        NATIONAL SECURITY INFRASTRUCTURE
                    </span>
                    <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6 bg-gradient-to-r from-white via-gray-200 to-gray-400 bg-clip-text text-transparent">
                        Behavioral Fraud <br className="hidden md:block" /> Intelligence Grid
                    </h1>
                    <p className="text-xl md:text-2xl text-zinc-400 max-w-3xl mx-auto mb-10 leading-relaxed">
                        Satark is India&apos;s first metadata-driven early warning system.
                        We detect coordinated campaigns, neutralize revenue fraud, and protect citizens—without listening to a single call.
                    </p>

                    <div className="flex flex-col md:flex-row gap-4 justify-center items-center">
                        <Button size="lg" className="h-14 px-8 text-lg font-bold shadow-[0_0_20px_rgba(100,255,218,0.3)] hover:shadow-[0_0_30px_rgba(100,255,218,0.5)] transition-all">
                            Access Intelligence Grid
                        </Button>
                        <Button variant="outline" size="lg" className="h-14 px-8 text-lg">
                            Read Architecture Whitepaper
                        </Button>
                    </div>
                </motion.div>

                <div className="grid md:grid-cols-3 gap-8 mt-24 text-left max-w-5xl mx-auto">
                    <FeatureCard
                        icon={EyeOff}
                        title="Privacy First"
                        desc="Metadata-only analysis. No voice recording, no content inspection. Zero surveillance architecture."
                    />
                    <FeatureCard
                        icon={Activity}
                        title="Pre-Crime Prediction"
                        desc="Detects fraud campaigns 14 minutes before the first victim report using behavioral vector analysis."
                    />
                    <FeatureCard
                        icon={ShieldCheck}
                        title="Telecom-Grade"
                        desc="Scales to 50,000 events/second. Integrated directly with core network switching fabric."
                    />
                </div>
            </div>

            {/* Background Grid */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]" />
            <div className="absolute inset-0 bg-gradient-to-t from-background via-background/80 to-transparent" />
        </section>
    )
}

function FeatureCard({ icon: Icon, title, desc }: any) {
    return (
        <motion.div
            whileHover={{ y: -5 }}
            className="p-6 rounded-2xl bg-card border border-border/50 hover:border-primary/50 transition-colors"
        >
            <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <Icon className="w-6 h-6 text-primary" />
            </div>
            <h3 className="text-xl font-bold mb-2 text-white">{title}</h3>
            <p className="text-zinc-400 leading-relaxed">{desc}</p>
        </motion.div>
    )
}
