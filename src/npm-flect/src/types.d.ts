export type Json =
  | string
  | number
  | boolean
  | null
  | Json[]
  | {
      [k: string]: Json;
    };

export type AnyComponentProps =
  | AvatarProps
  | ButtonProps
  | CodeBlockProps
  | ContainerProps
  | CopyButtonProps
  | CustomProps
  | DataGridProps
  | DialogProps
  | DisplayProps
  | FormProps
  | HeadingProps
  | LinkProps
  | MarkdownProps
  | NavLinkProps
  | OutletProps
  | ParagraphProps
  | TableProps
  | TextProps;

export type AnyActionProps =
  | NotifyActionProps
  | RedirectActionProps
  | DispatchEventActionProps;

export type ActionResponse = {
  action: AnyActionProps;
};
