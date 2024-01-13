import { cn } from "@/lib/utils";
import { cva, type VariantProps } from "class-variance-authority";

const LogoVariants = cva("font-Outfit", {
    variants: {
        size: {
            sm: "w-4 h-4 text-sm",
            md: "w-6 h-6 text-md",
            lg: "w-8 h-8 text-3xl",
        },
    },
    defaultVariants: {
        size: "md",
    },
});

export interface LogoProps extends VariantProps<typeof LogoVariants> {
    ctype: "logo";
    text: string;
}

export function Logo(props: LogoProps) {
    return <div className={cn(LogoVariants(props))}>{props.text}</div>;
}
