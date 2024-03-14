import {
  Button as ButtonUI,
  ButtonProps as ButtonPropsUI,
} from "@/components/ui/button";
import {
  AnyComponents,
  ComponentProps,
} from "@/components/flect/any-component";
import { AnyAction, executeAction } from "@/lib/action";

export interface ButtonProps extends Omit<ButtonPropsUI, "children"> {
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
