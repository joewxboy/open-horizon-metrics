export const getBackendSrv = jest.fn().mockReturnValue({
  datasourceRequest: jest.fn().mockResolvedValue({ data: [] }),
}); 