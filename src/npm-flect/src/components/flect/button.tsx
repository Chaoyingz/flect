import {
  Button as ButtonUI,
  ButtonProps as ButtonPropsUI,
} from "@/components/ui/button";
import { AnyComponents } from "@/components/flect/any-component";
import { AnyAction, executeAction } from "@/lib/action";
import { ComponentProps } from "@/types";

export interface ButtonProps extends Omit<ButtonPropsUI, "children"> {
  package: "flect";
  type: "button";
  onClickAction?: AnyAction;
  className?: string;
  children?: ComponentProps[];
}

export function Button({ children, onClickAction, ...rest }: ButtonProps) {
  const onClick = onClickAction
    ? () => executeAction(onClickAction)
    : undefined;
  return (
    <ButtonUI {...rest} onClick={onClick}>
      <AnyComponents children={children} />
    </ButtonUI>
  );
}
