import { createContext } from "react";

export interface ConfigContextState {
  debug?: boolean;
}

const defaultConfig: ConfigContextState = {
  debug: false,
};

export const ConfigContext = createContext<ConfigContextState>(defaultConfig);

export const ConfigProvider: React.FC<{
  children: React.ReactNode;
  config: ConfigContextState;
}> = ({ children, config }) => {
  return (
    <ConfigContext.Provider value={config}>{children}</ConfigContext.Provider>
  );
};
