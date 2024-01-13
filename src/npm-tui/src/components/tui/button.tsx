import {
    Button as ButtonUI,
    ButtonProps as ButtonPropsUI,
} from "@/components/ui/button";

export interface ButtonProps extends ButtonPropsUI {
    ctype: "button";
}

export function Button(props: ButtonProps) {
    return <ButtonUI {...props} />;
}
