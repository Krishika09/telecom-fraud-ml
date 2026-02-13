import { Navbar } from "@/components/Navbar";
import { HeroSection } from "@/components/HeroSection";
import { LiveThreatCounter } from "@/components/LiveThreatCounter";

export default function Home() {
  return (
    <main className="min-h-screen bg-background text-foreground overflow-x-hidden selection:bg-primary/30">
      <Navbar />
      <div className="pt-20">
        <HeroSection />
        <div className="container mx-auto px-4 pb-20">
          <LiveThreatCounter />
        </div>
      </div>

      <footer className="border-t border-white/5 py-12 bg-black/20">
        <div className="container mx-auto px-4 text-center text-zinc-500 text-sm">
          <p>&copy; 2026 Technically Correct. All rights reserved.</p>
          <div className="mt-4 space-x-6">
            <a href="#" className="hover:text-primary">Privacy Policy</a>
            <a href="#" className="hover:text-primary">Terms of Service</a>
            <a href="#" className="hover:text-primary">Government Directive 24-B</a>
          </div>
        </div>
      </footer>
    </main>
  );
}
