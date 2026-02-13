import { Sidebar } from "@/components/Sidebar";
import { SocketProvider } from "@/context/SocketContext";

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <SocketProvider>
            <div className="h-full relative">
                <div className="hidden h-full md:flex md:w-72 md:flex-col md:fixed md:inset-y-0 z-[80] bg-gray-900">
                    <Sidebar />
                </div>
                <main className="md:pl-72 h-full bg-background">
                    <div className="h-full p-8 overflow-y-auto">
                        {children}
                    </div>
                </main>
            </div>
        </SocketProvider>
    );
}
